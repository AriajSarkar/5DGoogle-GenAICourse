# Day 4a: Agent Observability - Logs, Traces & Metrics

## 📚 Overview

Agent observability provides complete visibility into your agent's decision-making process. Unlike traditional software that fails predictably, AI agents can fail mysteriously. Observability gives you the data to debug exactly why an agent failed, what prompts were sent to the LLM, which tools were available, and where failures occurred.

**Key Learning Outcomes:**
- ✅ Debug agent failures using DEBUG logs and ADK web UI
- ✅ Implement production observability with LoggingPlugin
- ✅ Create custom plugins for specialized metrics tracking
- ✅ Understand the core debugging pattern: symptom → logs → root cause → fix

## 🏗️ Foundational Pillars

### 1. **Logs** 
A record of a single event, telling you what happened at a specific moment.
- Example: "LLM Request sent with 242 tokens"
- Use case: Identify exactly which tool was called with what parameters

### 2. **Traces**
Connects logs into a single story, showing the entire sequence of steps.
- Example: User message → Agent starts → LLM call → Tool execution → Final response
- Use case: Understand complete agent workflow and identify bottlenecks

### 3. **Metrics**
Summary numbers (averages, error rates) showing overall performance.
- Example: "Agent made 4 LLM requests, 2 tool calls"
- Use case: Track cost, latency, and usage patterns over time

## 📖 Examples in This Module

### Example 1: `research_agent_debug/` - Debugging with ADK Web UI
**ADK App**: Interactive debugging with intentionally broken agent
```powershell
adk web --log_level DEBUG Day4/4a-agent-observability/
# Then select research_agent_debug from the agent dropdown in UI
```

**What it demonstrates:**
- Using `--log_level DEBUG` to see full LLM prompts and responses
- Inspecting function calls in ADK web UI Events tab
- Identifying type mismatch bugs (str vs List[str])
- Using Trace button to see timing information

**Debugging workflow:**
1. Run agent in ADK web UI
2. Notice incorrect count (e.g., 5000+ papers)
3. Click Events tab → Find `count_papers` function call
4. Inspect LLM Request → See papers passed as string, not list
5. Fix: Change `count_papers(papers: str)` to `count_papers(papers: List[str])`

**Standalone reference:** `01_debug_with_logs.py`

---

### Example 2: `logging_plugin_demo/` - Production Observability
**ADK App**: LoggingPlugin for automatic comprehensive logging
```powershell
adk run Day4/4a-agent-observability/logging_plugin_demo/
```

**What it demonstrates:**
- Using built-in `LoggingPlugin` for production systems
- Capturing all agent events: user messages, tool calls, LLM requests
- No code changes needed - just plugin registration
- Scaling observability beyond development

**Key code pattern:**
```python
from google.adk.plugins.logging_plugin import LoggingPlugin

runner = InMemoryRunner(
    agent=research_agent,
    plugins=[LoggingPlugin()]  # Automatic observability
)
```

**What LoggingPlugin captures:**
- 🚀 USER MESSAGE RECEIVED
- 🏃 INVOCATION STARTING
- 🤖 AGENT STARTING
- 🧠 LLM REQUEST (with system instruction and available tools)
- 🧠 LLM RESPONSE (with token usage)
- 🔧 TOOL STARTING/COMPLETED
- ✅ INVOCATION COMPLETED

**Standalone reference:** `02_logging_plugin.py`

---

### Example 3: `custom_plugin_demo/` - Custom Metrics Tracking
**ADK App**: Custom plugin for specialized observability needs
```powershell
adk run Day4/4a-agent-observability/custom_plugin_demo/
```

**What it demonstrates:**
- Creating custom plugins by extending `BasePlugin`
- Implementing `before_agent_callback` and `before_model_callback`
- Tracking custom metrics (invocation counts)
- Understanding when to use custom plugins vs LoggingPlugin

**Key code pattern:**
```python
from google.adk.plugins.base_plugin import BasePlugin

class CountInvocationPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="count_invocation")
        self.agent_count = 0
        self.llm_request_count = 0
    
    async def before_agent_callback(self, *, agent, callback_context):
        self.agent_count += 1
        logging.info(f"Agent run count: {self.agent_count}")
    
    async def before_model_callback(self, *, callback_context, llm_request):
        self.llm_request_count += 1
        logging.info(f"LLM request count: {self.llm_request_count}")

runner = InMemoryRunner(agent=agent, plugins=[CountInvocationPlugin()])
```

**Available callbacks:**
- `before/after_agent_callback` - Agent lifecycle hooks
- `before/after_tool_callback` - Tool execution hooks
- `before/after_model_callback` - LLM request hooks
- `on_model_error_callback` - Error handling hooks

**Standalone reference:** `03_custom_plugin.py`

---

## 🔧 Common Patterns

### Pattern 1: Development Debugging
**When:** Diagnosing failures during development

**How:**
```powershell
adk web --log_level DEBUG my_agent/
```

**What you get:**
- Interactive ADK web UI for testing
- Full LLM request/response in Events tab
- Trace visualization with timing
- Side-by-side comparison of actual vs expected

**Best for:** Understanding why an agent made a specific decision

---

### Pattern 2: Production Observability
**When:** Monitoring deployed agents in production

**How:**
```python
from google.adk.plugins.logging_plugin import LoggingPlugin

runner = InMemoryRunner(
    agent=agent,
    plugins=[LoggingPlugin()]
)
```

**What you get:**
- Comprehensive event logging
- User messages, tool calls, LLM requests
- Token usage tracking
- Complete execution traces

**Best for:** Standard production observability without custom code

---

### Pattern 3: Custom Metrics
**When:** Need business-specific tracking (cost, latency, security)

**How:**
```python
class CustomPlugin(BasePlugin):
    async def before_model_callback(self, *, callback_context, llm_request):
        # Track cost, latency, validate inputs, etc.
        pass

runner = InMemoryRunner(agent=agent, plugins=[CustomPlugin()])
```

**What you get:**
- Complete control over what to log
- Integration with external monitoring (DataDog, Prometheus)
- Business-specific metrics (cost per query, success rate)

**Best for:** Advanced use cases requiring custom logic

---

## 🎯 Decision Tree: Which Logging Approach?

```
┌─────────────────────────────────────┐
│ Need observability for your agent? │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ Development or Prod? │
    └──┬────────────────┬──┘
       │                │
  Development        Production
       │                │
       ▼                ▼
┌─────────────┐  ┌──────────────────┐
│ adk web     │  │ Standard logging │
│ --log_level │  │ or custom needs? │
│ DEBUG       │  └────┬─────────┬───┘
└─────────────┘       │         │
                  Standard    Custom
                      │         │
                      ▼         ▼
              ┌──────────┐  ┌─────────────┐
              │ Logging  │  │ Custom      │
              │ Plugin   │  │ Plugin      │
              └──────────┘  └─────────────┘
```

---

## 🚨 Common Issues & Solutions

### Issue 1: Agent gives wrong answer but no errors
**Symptom:** Agent responds but result is incorrect

**Debug with:**
```powershell
adk web --log_level DEBUG my_agent/
```

**Look for:**
- Events tab → Find tool calls with incorrect parameters
- Trace → Check which tools were called in what order
- LLM Response → See if model chose wrong function

**Example fix:** Update tool docstring to guide LLM better

---

### Issue 2: Need to track agent cost in production
**Symptom:** Want to measure token usage and cost per query

**Solution:** Use LoggingPlugin and parse token counts
```python
# LoggingPlugin outputs token usage:
# [logging_plugin] Token Usage - Input: 242, Output: 21

# Or build custom plugin:
class CostTrackingPlugin(BasePlugin):
    async def before_model_callback(self, *, llm_request, **kwargs):
        # Track request tokens
        pass
    
    async def after_model_callback(self, *, llm_response, **kwargs):
        # Track response tokens and calculate cost
        total_cost = (input_tokens * $X) + (output_tokens * $Y)
```

---

### Issue 3: Agent slow but don't know which step is bottleneck
**Symptom:** Agent takes too long to respond

**Debug with:** ADK web UI Trace feature
1. Run agent in `adk web`
2. Click Events tab → Click Trace button
3. See timing for each span (agent calls, tool calls, LLM requests)
4. Identify slowest step (e.g., LLM call taking 3s)

**Example fix:** Use faster model, optimize tool implementation, or add caching

---

## 📊 Quick Reference

### Log Levels
```python
logging.basicConfig(level=logging.DEBUG)  # All details
logging.basicConfig(level=logging.INFO)   # Important events
logging.basicConfig(level=logging.WARNING) # Warnings only
logging.basicConfig(level=logging.ERROR)  # Errors only
```

### ADK Web UI Commands
```powershell
# Development debugging
adk web --log_level DEBUG my_agent/

# Default (INFO level)
adk web my_agent/

# Custom port
adk web --port 8080 my_agent/
```

### Plugin Registration
```python
# Single plugin
runner = InMemoryRunner(agent=agent, plugins=[LoggingPlugin()])

# Multiple plugins
runner = InMemoryRunner(
    agent=agent,
    plugins=[LoggingPlugin(), CustomPlugin()]
)
```

---

## 🔗 Resources

**ADK Documentation:**
- [Observability Overview](https://developers.google.com/adk/docs/observability)
- [LoggingPlugin Reference](https://developers.google.com/adk/docs/plugins/logging-plugin)
- [Custom Plugins Guide](https://developers.google.com/adk/docs/plugins/custom-plugins)
- [External Integrations](https://developers.google.com/adk/docs/observability/integrations)

**Course Materials:**
- Day 3: Sessions & Memory (context for observability)
- Day 4b: Agent Evaluation (proactive vs reactive monitoring)

---

## 🎓 Key Takeaways

1. **Observability ≠ Just Logging**: It's logs + traces + metrics for complete visibility
2. **DEBUG logs are powerful**: Use `adk web --log_level DEBUG` to see full LLM prompts
3. **LoggingPlugin scales**: Zero-code production observability
4. **Custom plugins for custom needs**: Build when standard logging isn't enough
5. **Debugging pattern**: Symptom → Logs → Root cause → Fix → Verify

**Next:** Day 4b covers Agent Evaluation - proactive testing to catch issues before they reach production!
