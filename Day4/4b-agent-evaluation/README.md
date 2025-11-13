# Day 4b: Agent Evaluation

## 📚 Overview

Agent evaluation is the systematic process of testing and measuring how well an AI agent performs across different scenarios. Unlike traditional software testing, agents require evaluation of their entire decision-making process - including the final response AND the path taken to get there (trajectory).

**Why Evaluation Matters:**
- Agents are non-deterministic (different answers each time)
- Users give unpredictable, ambiguous commands
- Small prompt changes cause dramatic behavior shifts
- Need systematic evaluation, not just "happy path" testing

**Key Learning Outcomes:**
- ✅ Create test cases interactively in ADK web UI
- ✅ Run evaluations with response_match and tool_trajectory metrics
- ✅ Detect regressions using CLI-based batch testing
- ✅ Understand when to use static tests vs user simulation

## 🏗️ Evaluation Components

### 1. **Test Cases**
Pre-defined conversations with expected outcomes.
- User prompt: "Turn on the desk lamp in the office"
- Expected response: "Successfully set the desk lamp..."
- Expected tool calls: set_device_status(location="office", device_id="desk lamp", status="ON")

### 2. **Evaluation Metrics**
Measures of agent quality:
- **response_match_score**: Text similarity (0.0-1.0)
- **tool_trajectory_avg_score**: Correct tool usage (0.0-1.0)

### 3. **Evaluation Config**
Defines pass/fail thresholds:
```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

## 📖 Examples in This Module

### Example 1: `home_automation_eval/` - Interactive Web UI Evaluation
**ADK App**: Create and run test cases interactively
```powershell
adk web Day4/4b-agent-evaluation/
```

**What it demonstrates:**
- Creating test cases from conversations in ADK web UI
- Running evaluations with default metrics
- Analyzing pass/fail results in Evaluation History
- Side-by-side comparison of actual vs expected

**Interactive workflow:**
1. **Create test case:**
   - Have conversation: "Turn on the desk lamp in the office"
   - Click Eval tab → Create Evaluation set → Name it "home_tests"
   - Click ">" arrow → Add current session
   - Give case name: "basic_device_control"

2. **Run evaluation:**
   - Check your test case
   - Click "Run Evaluation" button
   - Leave default metrics, click "Start"
   - See green "Pass" in Evaluation History

3. **Practice failure analysis:**
   - Edit test case (pencil icon)
   - Change expected response to something wrong
   - Re-run evaluation
   - Hover over "Fail" → See Actual vs Expected comparison

**Standalone reference:** `01_interactive_evaluation.py`

---

### Example 2: `regression_testing/` - CLI-Based Batch Testing
**ADK App**: Automated regression testing with adk eval CLI
```powershell
adk eval Day4/4b-agent-evaluation/regression_testing/ Day4/4b-agent-evaluation/regression_testing/integration.evalset.json --config_file_path=Day4/4b-agent-evaluation/regression_testing/test_config.json --print_detailed_results
```

**What it demonstrates:**
- Creating evaluation config (test_config.json)
- Creating test cases programmatically (integration.evalset.json)
- Running batch evaluations via CLI
- Analyzing detailed results with --print_detailed_results

**File structure:**
```
regression_testing/
├── agent.py                     # Agent definition
├── test_config.json             # Pass/fail thresholds
└── integration.evalset.json     # Test cases
```

**test_config.json:**
```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,  // Exact tool match
    "response_match_score": 0.8        // 80% text similarity
  }
}
```

**integration.evalset.json structure:**
```json
{
  "eval_set_id": "regression_test_suite",
  "eval_cases": [
    {
      "eval_id": "basic_light_control",
      "conversation": [
        {
          "user_content": {"parts": [{"text": "Turn on the desk lamp"}]},
          "final_response": {"parts": [{"text": "Successfully set..."}]},
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "set_device_status",
                "args": {"location": "office", "device_id": "desk lamp", "status": "ON"}
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**CLI evaluation command:**
```powershell
adk eval agent_path/ evalset.json --config_file_path config.json --print_detailed_results
```

**Sample output:**
```
*********************************************************************
Eval Run Summary
regression_test_suite:
  Tests passed: 1
  Tests failed: 1
********************************************************************

Eval Id: basic_light_control
Overall Eval Status: PASSED
Metric: tool_trajectory_avg_score, Status: PASSED, Score: 1.0, Threshold: 1.0
Metric: response_match_score, Status: PASSED, Score: 0.95, Threshold: 0.8

Eval Id: bedroom_light_off
Overall Eval Status: FAILED
Metric: tool_trajectory_avg_score, Status: PASSED, Score: 1.0, Threshold: 1.0
Metric: response_match_score, Status: FAILED, Score: 0.65, Threshold: 0.8
```

**Standalone reference:** `02_cli_evaluation.py`

---

### Example 3: User Simulation (Conceptual Overview)
**Conceptual Guide**: Dynamic test case generation with LLM-powered user simulation

**What it demonstrates:**
- Limitations of static test cases
- How User Simulation works (ConversationScenario + LLM)
- When to use User Simulation vs static tests
- Conversation plan structure

**Key concepts:**
```python
# Conceptual example (see ADK docs for implementation)
scenario = ConversationScenario(
    scenario_id="home_automation_ambiguous",
    user_persona="A busy parent who wants to control lights",
    conversation_plan="""
    Goal: Turn on the desk lamp in the office
    
    Steps:
    1. Start with ambiguous request: "I need some light"
    2. If agent asks for clarification, provide room: "In the office"
    3. If agent asks which device, specify: "The desk lamp"
    4. Confirm the light is on
    """,
    expected_outcome="Desk lamp successfully turned on in office",
)
```

**Static vs User Simulation comparison:**

| Aspect | Static Tests | User Simulation |
|--------|-------------|-----------------|
| User prompts | Pre-defined | LLM-generated |
| Conversation flow | Fixed | Dynamic |
| Edge case discovery | Manual | Automatic |
| Setup complexity | Simple | Moderate |
| Execution time | Fast | Slower (LLM calls) |
| Cost | Low | Higher (LLM usage) |
| Reproducibility | Perfect | Varies |
| Best for | Regression testing | Comprehensive testing |

**When to use:**
- **Static tests**: CI/CD regression testing, known scenarios, fast validation
- **User Simulation**: Pre-release testing, edge case discovery, multi-turn validation

**Standalone reference:** `03_user_simulation.py` (conceptual guide)

---

## 🔧 Common Patterns

### Pattern 1: Interactive Test Creation
**When:** Creating baseline test cases during development

**How:**
1. Run `adk web my_agent/`
2. Have successful conversations
3. Save conversations as test cases in Eval tab
4. Run evaluations to establish baseline

**Best for:** Initial test suite creation, exploratory testing

---

### Pattern 2: Automated Regression Testing
**When:** CI/CD pipeline integration, nightly builds

**How:**
1. Create test_config.json with thresholds
2. Create integration.evalset.json with test cases
3. Run `adk eval agent/ evalset.json --config_file_path config.json`
4. Fail build if any tests fail

**Best for:** Preventing regressions, automated quality checks

---

### Pattern 3: Comprehensive Pre-Release Testing
**When:** Before major releases, after significant changes

**How:**
1. Run static tests first (fast regression check)
2. Add User Simulation for edge cases
3. Analyze failures and fix
4. Re-run evaluation suite

**Best for:** Thorough quality validation before production deployment

---

## 📊 Evaluation Metrics Deep Dive

### 1. response_match_score
**What it measures:** Text similarity between actual and expected response

**How it works:**
- Uses text similarity algorithms (e.g., cosine similarity)
- Compares actual agent response with expected response
- Score: 0.0 (completely different) to 1.0 (perfect match)

**Typical thresholds:**
- 0.9-1.0: Very strict (near-exact match required)
- 0.7-0.9: Moderate (allows natural variation)
- 0.5-0.7: Lenient (checks general meaning)

**Example:**
```
Expected: "Successfully set the desk lamp in the office to on."
Actual:   "The desk lamp in the office has been turned on."
Score:    0.85 (PASS if threshold is 0.8)
```

**When it fails:**
- Agent uses different phrasing
- Missing key information
- Extra irrelevant information

**How to fix:**
- Update agent instruction for consistent language
- Adjust threshold if variation is acceptable
- Use more flexible expected responses

---

### 2. tool_trajectory_avg_score
**What it measures:** Correct tool usage with correct parameters

**How it works:**
- Compares actual tool calls with expected tool calls
- Checks: tool name, parameter names, parameter values
- Score: 0.0 (wrong tools) to 1.0 (perfect match)

**Typical thresholds:**
- 1.0: Exact match required (most common)
- 0.8-0.9: Allow minor parameter variations

**Example:**
```
Expected: set_device_status(location="office", device_id="desk lamp", status="ON")
Actual:   set_device_status(location="office", device_id="desk lamp", status="ON")
Score:    1.0 (PASS)

Expected: set_device_status(location="office", device_id="desk lamp", status="ON")
Actual:   set_device_status(location="bedroom", device_id="desk lamp", status="ON")
Score:    0.0 (FAIL - wrong location)
```

**When it fails:**
- Agent calls wrong tool
- Correct tool but wrong parameters
- Missing required tool calls
- Extra unnecessary tool calls

**How to fix:**
- Update tool docstrings to guide LLM better
- Improve agent instruction clarity
- Add examples to instruction
- Verify tool discovery (check available tools in DEBUG logs)

---

## 🚨 Common Issues & Solutions

### Issue 1: All tests fail with low response_match_score
**Symptom:** Every test fails, scores all around 0.3-0.5

**Root cause:** Agent response format changed but expected responses didn't

**Solution:**
```powershell
# Re-create baseline by running conversations in ADK web UI
adk web my_agent/

# Update expected responses in evalset.json
# Or adjust threshold in test_config.json if new format is acceptable
{
  "criteria": {
    "response_match_score": 0.6  // Lower threshold
  }
}
```

---

### Issue 2: tool_trajectory fails but agent seems correct
**Symptom:** Score 0.0 but tool call looks right in logs

**Root cause:** Parameter order or naming mismatch

**Debug:**
```powershell
# Use --print_detailed_results to see exact diff
adk eval agent/ evalset.json --config_file_path config.json --print_detailed_results

# Look at "expected_tool_calls" vs "actual_tool_calls" columns
```

**Example issue:**
```
Expected: {"location": "office", "device_id": "lamp", "status": "ON"}
Actual:   {"device_id": "lamp", "location": "office", "status": "ON"}
```

**Solution:** Update expected tool calls in evalset.json to match actual parameter order

---

### Issue 3: Need to test multi-turn conversations
**Symptom:** Agent works in single-turn but fails in context retention

**Solution:** Use multi-turn conversation in evalset.json
```json
{
  "eval_id": "multi_turn_context",
  "conversation": [
    {
      "user_content": {"parts": [{"text": "Turn on the light"}]},
      "final_response": {"parts": [{"text": "Which room?"}]}
    },
    {
      "user_content": {"parts": [{"text": "The office"}]},
      "final_response": {"parts": [{"text": "Which device?"}]}
    },
    {
      "user_content": {"parts": [{"text": "The desk lamp"}]},
      "final_response": {"parts": [{"text": "Successfully set..."}]},
      "intermediate_data": {
        "tool_uses": [
          {"name": "set_device_status", "args": {...}}
        ]
      }
    }
  ]
}
```

---

## 📊 Quick Reference

### ADK Eval CLI Commands
```powershell
# Basic evaluation
adk eval agent_path/ evalset.json

# With config file
adk eval agent_path/ evalset.json --config_file_path test_config.json

# With detailed results
adk eval agent_path/ evalset.json --config_file_path test_config.json --print_detailed_results

# Multiple evalsets
adk eval agent_path/ evalset1.json evalset2.json --config_file_path test_config.json
```

### Evaluation File Formats

**test_config.json:**
```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

**integration.evalset.json:**
```json
{
  "eval_set_id": "unique_suite_name",
  "eval_cases": [
    {
      "eval_id": "unique_test_name",
      "conversation": [
        {
          "user_content": {"parts": [{"text": "user prompt"}]},
          "final_response": {"parts": [{"text": "expected response"}]},
          "intermediate_data": {
            "tool_uses": [
              {"name": "tool_name", "args": {"param": "value"}}
            ]
          }
        }
      ]
    }
  ]
}
```

### Threshold Guidelines

| Metric | Strict | Moderate | Lenient | Use Case |
|--------|--------|----------|---------|----------|
| response_match | 0.9+ | 0.7-0.9 | 0.5-0.7 | Critical messaging vs general helpfulness |
| tool_trajectory | 1.0 | 0.8-0.9 | 0.6-0.8 | Exact operations vs flexible workflows |

---

## 🔗 Resources

**ADK Documentation:**
- [Evaluation Overview](https://developers.google.com/adk/docs/evaluation)
- [Evaluation Criteria](https://developers.google.com/adk/docs/evaluation/criteria)
- [User Simulation](https://developers.google.com/adk/docs/evaluation/user-simulation)
- [Pytest Evaluation](https://developers.google.com/adk/docs/evaluation/pytest)
- [Advanced Evaluation](https://developers.google.com/adk/docs/evaluation/advanced)

**Course Materials:**
- Day 4a: Agent Observability (reactive debugging)
- Day 3: Sessions & Memory (context for conversation evaluation)

---

## 🎓 Key Takeaways

1. **Evaluation ≠ Just Testing**: It's systematic measurement of agent quality across dimensions
2. **Two key metrics**: response_match (communication) + tool_trajectory (functionality)
3. **Interactive → Automated**: Start with ADK web UI, scale to CLI evaluation
4. **Static tests for regression**: Fast, reproducible, CI/CD friendly
5. **User Simulation for comprehensive testing**: Uncover edge cases, validate multi-turn flows
6. **Observability + Evaluation = Quality**: Reactive (Day 4a) + Proactive (Day 4b)

**Next:** Day 5 will cover deploying agents to production and advanced topics like Agent2Agent protocol!
