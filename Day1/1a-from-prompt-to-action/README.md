# Day 1a: From Prompt to Action

**Learn AI agent fundamentals and build agents with custom tools!**

---

## 🎯 What You'll Learn

By the end of this module, you will:

- ✅ Understand what AI agents are (vs. simple LLMs)
- ✅ Create basic agents with Google ADK
- ✅ Build custom Python function tools
- ✅ Use built-in tools (Google Search)
- ✅ Combine multiple tools in one agent
- ✅ Build interactive conversational agents

---

## 📚 Module Scripts (Run in Order!)

| Script | Topic | What It Teaches |
|--------|-------|-----------------|
| **01_basic_agent.py** | Basic Agent | Agent lifecycle, InMemoryRunner, simple Q&A |
| **02_agent_with_custom_tool.py** | Custom Tools | Creating Python functions as tools, docstrings |
| **03_agent_with_google_search.py** | Built-in Tools | Using GoogleSearchTool for web queries |
| **04_multi_tool_agent.py** | Multiple Tools | Combining custom + built-in tools |
| **05_interactive_agent.py** | Conversations | Multi-turn interactions, session state |

---

## 🚀 Quick Start

### Prerequisites

Make sure you've completed the main setup from the root folder:

```powershell
# From Google-Course root:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GOOGLE_API_KEY="your-key-here"
```

**Haven't done setup?** → See [../../SETUP.md](../../SETUP.md)

### Run Your First Script!

```powershell
# Make sure you're in the Day 1a folder
cd Day1/1a-from-prompt-to-action

# Run the first example
python 01_basic_agent.py
```

You should see the agent respond to a question! 🎉

---

## 📖 Learning Path

### Step 1: Basic Agent (01_basic_agent.py)

**What it teaches:**
- Creating an `Agent` instance
- Setting up `InMemoryRunner`
- Running agents with `run_debug()`
- Understanding agent responses

**Key Code:**
```python
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner

agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant."
)

runner = InMemoryRunner(agent=agent)
response = await runner.run_debug("Your question")
```

**Try it:**
- Modify the instruction
- Ask different questions
- See how the agent adapts

---

### Step 2: Custom Tools (02_agent_with_custom_tool.py)

**What it teaches:**
- Creating Python functions as tools
- Writing effective docstrings
- How agents decide when to use tools
- Tool parameter passing

**Key Concept:** 
Agents can call Python functions! The function's docstring tells the agent what it does.

**Example Tool:**
```python
def calculate_area(length: float, width: float) -> dict:
    """
    Calculate the area of a rectangle.
    
    Args:
        length: Length of the rectangle
        width: Width of the rectangle
    
    Returns:
        dict: Contains the calculated area
    """
    area = length * width
    return {"area": area, "unit": "square units"}
```

**Try it:**
- Create your own calculator tools
- Add more math functions
- See when the agent chooses to use each tool

---

### Step 3: Google Search Tool (03_agent_with_google_search.py)

**What it teaches:**
- Using built-in ADK tools
- GoogleSearchTool for web queries
- Real-time information retrieval
- Grounding responses in facts

**Key Code:**
```python
from google.adk.tools.google_search_tool import GoogleSearchTool

agent = Agent(
    name="researcher",
    model="gemini-2.5-flash",
    tools=[GoogleSearchTool()],  # Built-in search!
)
```

**Try it:**
- Ask current events questions
- Compare answers with/without search
- See how agents verify information

---

### Step 4: Multi-Tool Agent (04_multi_tool_agent.py)

**What it teaches:**
- Combining multiple tools
- Agent tool selection logic
- Creating tool "ecosystems"
- Handling complex queries

**Example:**
```python
def get_time(city: str) -> str:
    """Get current time in a city."""
    # ... timezone logic ...

agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    tools=[
        get_time,           # Custom tool
        GoogleSearchTool()  # Built-in tool
    ]
)
```

**Try it:**
- Add weather tools
- Create unit converters
- Build a research assistant

---

### Step 5: Interactive Agent (05_interactive_agent.py)

**What it teaches:**
- Multi-turn conversations
- Session management
- Maintaining context
- Building chat applications

**Key Concept:**
Agents remember previous messages in a session!

**Try it:**
- Have multi-turn conversations
- Test context retention
- Build a customer support agent

---

## 🔑 Key Concepts

### What is an AI Agent?

**Simple LLM:**
- Input → LLM → Output
- No actions, just text

**AI Agent:**
- Input → **Think** (LLM) → **Act** (Tools) → **Observe** (Results) → Output
- Can take actions in the world!

### The Agent Lifecycle

```
1. USER INPUT
   ↓
2. AGENT THINKS (LLM analyzes input)
   ↓
3. AGENT DECIDES (Use tool? Which one?)
   ↓
4. AGENT ACTS (Calls Python function/API)
   ↓
5. AGENT OBSERVES (Sees tool results)
   ↓
6. AGENT RESPONDS (Synthesizes final answer)
```

### ADK Core Components

| Component | What It Does |
|-----------|--------------|
| **Agent** | The AI brain - decides what to do |
| **Tools** | Actions the agent can take (Python functions) |
| **Runner** | Orchestrates agent execution |
| **Session** | Maintains conversation history |

---

## 💡 Best Practices

### Writing Good Tools

✅ **DO:**
- Write clear, descriptive docstrings
- Use type hints for parameters
- Return structured data (dicts)
- Handle errors gracefully

❌ **DON'T:**
- Make tools too complex
- Forget docstrings (agent won't know what tool does!)
- Return unstructured strings
- Assume tool will always be called

### Example: Good vs. Bad Tool

**❌ Bad Tool:**
```python
def calc(a, b):  # No docstring! No types!
    return a * b  # What does this calculate?
```

**✅ Good Tool:**
```python
def calculate_area(length: float, width: float) -> dict:
    """
    Calculate the area of a rectangle.
    
    Args:
        length: The length of the rectangle in meters
        width: The width of the rectangle in meters
    
    Returns:
        dict: Contains 'area' in square meters
    """
    return {"area": length * width, "unit": "square meters"}
```

---

## 🛠️ Common Patterns

### Pattern 1: Simple Question Answering

```python
agent = Agent(
    name="qa_agent",
    model="gemini-2.5-flash",
    instruction="Answer questions clearly and concisely."
)
```

**Use for:** FAQs, general knowledge, simple tasks

---

### Pattern 2: Tool-Powered Agent

```python
agent = Agent(
    name="calculator",
    model="gemini-2.5-flash",
    tools=[add, subtract, multiply, divide],
    instruction="Help with math. Use tools for calculations."
)
```

**Use for:** Calculations, data processing, API calls

---

### Pattern 3: Research Agent

```python
agent = Agent(
    name="researcher",
    model="gemini-2.5-flash",
    tools=[GoogleSearchTool()],
    instruction="Research topics and provide verified information."
)
```

**Use for:** Current events, fact-checking, research

---

## 🐛 Troubleshooting

### Issue: "API key not found"

**Solution:**
```powershell
# Set the environment variable
$env:GOOGLE_API_KEY="your-key-here"

# Or create .env file in root:
echo 'GOOGLE_API_KEY=your-key-here' > ../../.env
```

### Issue: "Tool not called"

**Possible causes:**
1. Missing docstring - agent doesn't know what tool does
2. Unclear docstring - agent doesn't understand when to use it
3. Question doesn't require tool - agent answered directly

**Solution:** Write clearer docstrings that explain:
- What the tool does
- When to use it
- What parameters mean

### Issue: "Module not found"

**Solution:**
```powershell
# Make sure virtual environment is activated!
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r ../../requirements.txt
```

---

## 🎯 Learning Checkpoints

After completing this module, you should be able to:

- [ ] Explain what an AI agent is
- [ ] Create a basic agent with ADK
- [ ] Write a custom Python function tool
- [ ] Use GoogleSearchTool for web queries
- [ ] Combine multiple tools in one agent
- [ ] Build an interactive chat agent
- [ ] Understand when agents use tools vs. LLM knowledge

---

## 📝 Practice Exercises

### Beginner:
1. Modify `01_basic_agent.py` to answer questions about your favorite topic
2. Create a temperature converter tool (Celsius ↔ Fahrenheit)
3. Build a unit converter (km ↔ miles)

### Intermediate:
4. Create a multi-tool calculator (add, subtract, multiply, divide, power, sqrt)
5. Build a research agent that searches and summarizes findings
6. Make an interactive study assistant

### Advanced:
7. Create a personal assistant with time, search, and custom tools
8. Build a code helper that can search documentation
9. Design a travel agent with multiple specialized tools

---

## 🚀 Next Steps

**Completed Day 1a?** Great! Now:

1. **Practice:** Build your own agent with custom tools
2. **Move to Day 1b:** Learn [multi-agent architectures](../1b-agent-architectures/)
3. **Experiment:** Try different models, tools, and instructions

---

## 📚 Additional Resources

- **Main Course:** [../../README.md](../../README.md)
- **Setup Guide:** [../../SETUP.md](../../SETUP.md)
- **Quick Reference:** [../../QUICK_REFERENCE.md](../../QUICK_REFERENCE.md)
- **Day 1b (Next):** [../1b-agent-architectures/](../1b-agent-architectures/)

---

**Questions? Stuck? Check the troubleshooting section above or the main SETUP.md!**

**Ready for multi-agent systems? → [Go to Day 1b](../1b-agent-architectures/)**

---

<sub>**Module:** Day 1a | **Model:** gemini-2.5-flash | **Difficulty:** Beginner</sub>
