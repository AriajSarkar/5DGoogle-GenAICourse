# Day 1b: Agent Architectures

**Master multi-agent systems and workflow patterns!**

---

## 🎯 What You'll Learn

By the end of this module, you will:

- ✅ Understand why multi-agent > monolithic systems
- ✅ Master 4 essential workflow patterns
- ✅ Choose the right pattern for your use case
- ✅ Build LLM-based coordinators
- ✅ Create sequential workflows (assembly lines)
- ✅ Implement parallel execution
- ✅ Design iterative refinement loops

---

## 📚 Module Scripts (Run in Order!)

| Script | Pattern | What It Teaches |
|--------|---------|-----------------|
| **01_llm_coordinator_pattern.py** | LLM-Based | Dynamic routing with AgentTool |
| **02_sequential_pattern.py** | Sequential | Fixed-order workflows (A → B → C) |
| **03_parallel_pattern.py** | Parallel | Concurrent independent execution |
| **04_loop_pattern.py** | Loop | Iterative refinement with feedback |
| **05_pattern_comparison.py** | All 4 | Side-by-side pattern comparison |

---

## 🚀 Quick Start

### Prerequisites

```powershell
# Make sure you completed Day 1a first!
# And have the virtual environment set up:
.\.venv\Scripts\Activate.ps1
$env:GOOGLE_API_KEY="your-key-here"
```

### Run Your First Multi-Agent System!

```powershell
cd Day1/1b-agent-architectures
python 01_llm_coordinator_pattern.py
```

---

## 🏗️ The Four Workflow Patterns

### Pattern 1: LLM-Based Coordinator 🧠

**How it works:**
- A main "coordinator" agent decides which sub-agent to call
- Sub-agents are wrapped as `AgentTool`s
- LLM makes routing decisions dynamically

**When to use:**
- Complex decision-making needed
- Task routing changes based on context
- Need intelligent delegation

**Example Use Cases:**
- Customer support (route to billing, technical, sales agents)
- Content creation (writer, editor, publisher)
- Research assistant (searcher, analyzer, summarizer)

**Pros:**
- ✅ Flexible, intelligent routing
- ✅ Adapts to context
- ✅ Can handle unexpected scenarios

**Cons:**
- ❌ Slower (extra LLM calls)
- ❌ Less predictable
- ❌ Higher API costs

**Code Pattern:**
```python
from google.adk.agents import Agent
from google.adk.tools import AgentTool

# Sub-agents
writer = Agent(name="writer", model="gemini-2.5-flash")
editor = Agent(name="editor", model="gemini-2.5-flash")

# Wrap as tools
writer_tool = AgentTool(agent=writer)
editor_tool = AgentTool(agent=editor)

# Coordinator decides which to call
coordinator = Agent(
    name="coordinator",
    model="gemini-2.5-flash",
    tools=[writer_tool, editor_tool],
    instruction="Route tasks to the right specialist"
)
```

---

### Pattern 2: Sequential (Assembly Line) 🏭

**How it works:**
- Agents run in fixed order: A → B → C
- Each agent's output becomes next agent's input
- Deterministic, predictable flow

**When to use:**
- Clear step-by-step process
- Each step depends on previous
- Order matters

**Example Use Cases:**
- Blog creation: Outline → Write → Edit
- Code generation: Plan → Code → Review
- Data pipeline: Extract → Transform → Load

**Pros:**
- ✅ Fast (no routing overhead)
- ✅ Predictable
- ✅ Easy to debug
- ✅ Lower cost

**Cons:**
- ❌ Inflexible
- ❌ Can't skip steps
- ❌ Fixed order only

**Code Pattern:**
```python
from google.adk.agents import Agent, SequentialAgent

researcher = Agent(name="researcher", model="gemini-2.5-flash")
writer = Agent(name="writer", model="gemini-2.5-flash")
editor = Agent(name="editor", model="gemini-2.5-flash")

pipeline = SequentialAgent(
    name="content_pipeline",
    agents=[researcher, writer, editor]  # Fixed order!
)
```

---

### Pattern 3: Parallel (Concurrent) ⚡

**How it works:**
- Multiple agents run at the same time
- Each gets the same input
- All run independently
- Results combined at the end

**When to use:**
- Tasks are independent
- Need speed
- Multiple perspectives needed

**Example Use Cases:**
- Quality checks: Grammar + Facts + Style (all at once)
- Code review: Security + Performance + Style
- Multi-perspective analysis

**Pros:**
- ✅ Fastest execution
- ✅ Independent processing
- ✅ Fault tolerant

**Cons:**
- ❌ Can't share state during execution
- ❌ All agents run every time (can't skip)

**Code Pattern:**
```python
from google.adk.agents import Agent, ParallelAgent

grammar_checker = Agent(name="grammar", model="gemini-2.5-flash")
fact_checker = Agent(name="facts", model="gemini-2.5-flash")
style_checker = Agent(name="style", model="gemini-2.5-flash")

quality_control = ParallelAgent(
    name="qc_team",
    agents=[grammar_checker, fact_checker, style_checker]  # Run concurrently!
)
```

---

### Pattern 4: Loop (Iterative Refinement) 🔄

**How it works:**
- Two agents: Generator + Critic
- Generator creates, critic evaluates
- Loops until termination condition met
- Iterative improvement

**When to use:**
- Quality matters more than speed
- Need refinement through feedback
- Approval process required

**Example Use Cases:**
- Creative writing: Write → Critique → Rewrite → ...
- Code generation: Generate → Test → Fix → ...
- Design iteration: Propose → Review → Refine → ...

**Pros:**
- ✅ High quality outputs
- ✅ Self-improving
- ✅ Can achieve complex goals

**Cons:**
- ❌ Can be slow (multiple iterations)
- ❌ Need good termination condition
- ❌ Risk of infinite loops

**Code Pattern:**
```python
from google.adk.agents import Agent, LoopAgent

generator = Agent(name="generator", model="gemini-2.5-flash")
critic = Agent(
    name="critic",
    model="gemini-2.5-flash",
    instruction="Review and say APPROVED if good, else suggest improvements"
)

refiner = LoopAgent(
    name="refiner",
    agents=[generator, critic],
    termination_condition=lambda history: "APPROVED" in history[-1].content
)
```

---

## 🎯 Pattern Decision Tree

```
Need multiple agents?
│
├─ Tasks independent & need speed?
│  └─ Use PARALLEL
│
├─ Fixed order required (A → B → C)?
│  └─ Use SEQUENTIAL
│
├─ Need iterative improvement?
│  └─ Use LOOP
│
└─ Complex routing logic?
   └─ Use LLM COORDINATOR
```

---

## 📊 Pattern Comparison

| Feature | LLM Coordinator | Sequential | Parallel | Loop |
|---------|----------------|------------|----------|------|
| **Speed** | Slow | Fast | Fastest | Variable |
| **Flexibility** | High | Low | Low | Medium |
| **Cost** | High | Low | Medium | Variable |
| **Use Case** | Smart routing | Assembly line | Independent tasks | Refinement |
| **Predictability** | Low | High | High | Medium |
| **Complexity** | High | Low | Low | Medium |

---

## 💡 Real-World Examples

### Blog Creation System

```
LLM Coordinator:
  User asks question
    → Coordinator routes to:
      - Topic Expert (for ideas)
      - Writer (for draft)
      - SEO Specialist (for optimization)

Sequential:
  Research → Write → Edit → Format → Publish

Parallel:
  Grammar Check + Fact Check + Style Check (all at once)

Loop:
  Generate Draft → Critique → Revise → Critique → APPROVED
```

### Software Development

```
LLM Coordinator:
  Bug report → Route to:
    - Backend Dev
    - Frontend Dev
    - Database Admin

Sequential:
  Design → Code → Test → Deploy

Parallel:
  Security Audit + Performance Test + Code Review

Loop:
  Write Code → Run Tests → Fix Bugs → Run Tests → PASSED
```

---

## 🔑 Key Concepts

### AgentTool (LLM Coordinator Only)

Wraps a sub-agent as a tool that the coordinator can call:

```python
from google.adk.tools import AgentTool

sub_agent = Agent(name="specialist", model="gemini-2.5-flash")
tool = AgentTool(agent=sub_agent)

coordinator = Agent(
    name="manager",
    model="gemini-2.5-flash",
    tools=[tool]  # LLM decides when to call sub-agent
)
```

### Termination Conditions (Loop Pattern)

Define when to stop looping:

```python
# Stop when "APPROVED" appears
termination = lambda history: "APPROVED" in history[-1].content

# Stop after max iterations
counter = 0
termination = lambda h: counter >= 5 or "APPROVED" in h[-1].content
```

### State Management

- **Sequential:** Each agent sees previous agent's output
- **Parallel:** Each agent sees original input only
- **Loop:** Agents see full conversation history
- **Coordinator:** Sub-agents see only coordinator's delegation

---

## 🛠️ Common Patterns & Best Practices

### Pattern: Content Quality Pipeline

```python
# Sequential for main flow
outline_agent = Agent(...)
writer_agent = Agent(...)
editor_agent = Agent(...)

pipeline = SequentialAgent(agents=[outline_agent, writer_agent, editor_agent])

# Then parallel for quality checks
grammar = Agent(...)
facts = Agent(...)
style = Agent(...)

qc = ParallelAgent(agents=[grammar, facts, style])

# Combine both!
```

### Pattern: Smart Router with Fallback

```python
# Try specialist first, fallback to generalist
specialist_tool = AgentTool(agent=specialist)
generalist_tool = AgentTool(agent=generalist)

router = Agent(
    tools=[specialist_tool, generalist_tool],
    instruction="Try specialist first, use generalist if specialist can't help"
)
```

### Pattern: Loop with Max Iterations

```python
max_iterations = 3
iteration_count = 0

def terminate(history):
    global iteration_count
    iteration_count += 1
    return "APPROVED" in history[-1].content or iteration_count >= max_iterations

loop = LoopAgent(agents=[gen, critic], termination_condition=terminate)
```

---

## 🐛 Troubleshooting

### Issue: Sequential agents in wrong order

**Problem:** Agents run in wrong sequence

**Solution:** Check the `agents=[]` list order:
```python
# ✅ Correct order
SequentialAgent(agents=[first, second, third])

# ❌ Wrong order
SequentialAgent(agents=[third, first, second])
```

### Issue: Parallel agents not actually parallel

**Problem:** Seem to run sequentially

**Solution:** They ARE running in parallel! ADK handles this automatically. The console output may appear sequential, but execution is concurrent.

### Issue: Loop never terminates

**Problem:** Loop runs forever

**Solution:** Add better termination condition:
```python
# ❌ Bad - might never see exact string
lambda h: "APPROVED" in h[-1].content

# ✅ Better - multiple conditions
lambda h: ("APPROVED" in h[-1].content or 
           "LOOKS GOOD" in h[-1].content or
           len(h) > 10)  # Max 10 iterations
```

### Issue: Coordinator not calling sub-agents

**Problem:** Coordinator answers directly instead of delegating

**Solution:** Make instructions clearer:
```python
# ❌ Vague
instruction="Help the user"

# ✅ Clear
instruction="You are a manager. ALWAYS delegate tasks to specialist agents. Use writer_agent for content, editor_agent for revisions."
```

---

## 🎯 Learning Checkpoints

After this module, you should be able to:

- [ ] Explain when to use each pattern
- [ ] Build an LLM-based coordinator
- [ ] Create sequential workflows
- [ ] Implement parallel execution
- [ ] Design loop patterns with termination
- [ ] Combine patterns for complex systems
- [ ] Choose the right pattern for a use case

---

## 📝 Practice Exercises

### Beginner:
1. Modify `02_sequential_pattern.py` to add a 4th step
2. Create a parallel agent for code review (style + security + performance)
3. Build a simple loop that iterates exactly 3 times

### Intermediate:
4. Create a blog pipeline: Research → Outline → Write → Edit (sequential)
5. Build a coordinator that routes math vs. text questions
6. Make a loop that generates and tests code until tests pass

### Advanced:
7. Combine patterns: Coordinator → Sequential → Parallel
8. Build a customer support system with routing + escalation
9. Create a code assistant with generate → test → fix loop

---

## 🚀 Next Steps

**Completed Day 1b?** Congratulations! You now know:

- ✅ Single-agent systems (Day 1a)
- ✅ Multi-agent workflows (Day 1b)

**What's next:**
1. **Build a real project** combining both days
2. **Experiment** with different patterns
3. **Wait for Day 2** (coming soon!)

---

## 📚 Additional Resources

- **Day 1a:** [../1a-from-prompt-to-action/](../1a-from-prompt-to-action/)
- **Main Course:** [../../README.md](../../README.md)
- **Quick Reference:** [../../QUICK_REFERENCE.md](../../QUICK_REFERENCE.md)
- **Visual Guide:** [VISUAL_GUIDE.md](VISUAL_GUIDE.md)

---

**Ready to build your own multi-agent system? You have all the tools!** 🚀

---

<sub>**Module:** Day 1b | **Model:** gemini-2.5-flash | **Difficulty:** Intermediate</sub>
