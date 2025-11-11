# Running ADK Agents - Two Approaches

This course now provides agents in **ADK App Structure** - ready to use with `adk run`!

## 📁 New Structure

Each example now has a folder with the proper ADK structure:

```
Day1/1a-from-prompt-to-action/
├── basic_agent/                    # adk run Day1/1a-from-prompt-to-action/basic_agent
│   ├── __init__.py
│   └── agent.py
├── agent_with_custom_tool/        # adk run Day1/1a-from-prompt-to-action/agent_with_custom_tool
│   ├── __init__.py
│   └── agent.py
├── google_search_agent/           # adk run Day1/1a-from-prompt-to-action/google_search_agent
│   ├── __init__.py
│   └── agent.py
└── multi_tool_agent/              # adk run Day1/1a-from-prompt-to-action/multi_tool_agent
    ├── __init__.py
    └── agent.py

Day1/1b-agent-architectures/
├── llm_coordinator/               # adk run Day1/1b-agent-architectures/llm_coordinator
│   ├── __init__.py
│   └── agent.py
├── sequential_pattern/            # adk run Day1/1b-agent-architectures/sequential_pattern
│   ├── __init__.py
│   └── agent.py
├── parallel_pattern/              # adk run Day1/1b-agent-architectures/parallel_pattern
│   ├── __init__.py
│   └── agent.py
└── loop_pattern/                  # adk run Day1/1b-agent-architectures/loop_pattern
    ├── __init__.py
    └── agent.py
```

## 🚀 How to Run

### Method 1: Interactive CLI (Recommended)

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run any agent interactively
adk run Day1/1a-from-prompt-to-action/basic_agent

# Try different agents
adk run Day1/1a-from-prompt-to-action/agent_with_custom_tool
adk run Day1/1b-agent-architectures/sequential_pattern
adk run Day1/1b-agent-architectures/parallel_pattern
```

This gives you an **interactive chat interface** where you can:
- Ask multiple questions
- See the agent use tools in real-time
- Type `exit` or `quit` to stop

### Method 2: Web UI

```powershell
# Start web interface for any agent
adk web Day1/1a-from-prompt-to-action/
```

Opens a browser-based UI at `http://localhost:8000`

### Method 3: API Server

```powershell
# Start REST API server
adk api_server Day1/1a-from-prompt-to-action/basic_agent
```

Creates API endpoints for your agent

### Method 4: Python Script (For Learning)

The old standalone `.py` files are kept for reference and learning:

```powershell
python Day1/1a-from-prompt-to-action/01_basic_agent.py
python Day1/1b-agent-architectures/02_sequential_pattern.py
```

## 📚 Agent Overview

### Day 1a: Basic Agents

| Folder | What It Does | Key Concepts |
|--------|--------------|--------------|
| `basic_agent` | Simple Q&A agent | Agent basics, no tools |
| `agent_with_custom_tool` | Time & weather tools | Custom Python functions as tools |
| `google_search_agent` | Web search capability | Built-in GoogleSearchTool |
| `multi_tool_agent` | Multiple tools combined | Tool selection, complex tasks |

### Day 1b: Multi-Agent Patterns

| Folder | Pattern | What It Does |
|--------|---------|--------------|
| `llm_coordinator` | LLM-Based Coordinator | Dynamic routing via AgentTool |
| `sequential_pattern` | Sequential | Pipeline: Outline → Write → Edit |
| `parallel_pattern` | Parallel | Concurrent research + aggregation |
| `loop_pattern` | Loop | Iterative refinement with feedback |

## 🎯 Quick Examples

```powershell
# Example 1: Ask about time in different cities
adk run Day1/1a-from-prompt-to-action/agent_with_custom_tool
# Try: "What time is it in Tokyo and London?"

# Example 2: Create a blog post with sequential pipeline
adk run Day1/1b-agent-architectures/sequential_pattern
# Try: "Write a blog post about AI agents"

# Example 3: Parallel research on multiple topics
adk run Day1/1b-agent-architectures/parallel_pattern
# Try: "Research the latest trends in AI"

# Example 4: Iterative story refinement
adk run Day1/1b-agent-architectures/loop_pattern
# Try: "Write a short story about a robot learning to paint"
```

## 🔧 Troubleshooting

### "adk: command not found"
Make sure virtual environment is activated:
```powershell
.\.venv\Scripts\Activate.ps1
```

### "Invalid value for 'AGENT': Directory '...' is a file"
Use the **folder name**, not the .py file:
- ❌ `adk run Day1/1a-from-prompt-to-action/01_basic_agent.py`
- ✅ `adk run Day1/1a-from-prompt-to-action/basic_agent`

### API Key Not Set
```powershell
# Set temporarily
$env:GOOGLE_API_KEY="your-key-here"

# Or create .env file in agent folder
echo "GOOGLE_API_KEY=your-key-here" > Day1/1a-from-prompt-to-action/basic_agent/.env
```

## 📖 Learning Path

1. **Start with basic_agent** - Understand agent structure
2. **Try agent_with_custom_tool** - Learn how tools work
3. **Explore google_search_agent** - See built-in tools
4. **Test multi_tool_agent** - Watch agent choose tools
5. **Move to Day 1b patterns** - Build multi-agent systems

## 💡 Benefits of ADK App Structure

✅ **Interactive CLI** - Chat with your agent live  
✅ **Web UI** - Beautiful browser interface  
✅ **API Server** - Deploy as REST API  
✅ **Session Management** - Built-in conversation history  
✅ **Production Ready** - Proper project structure  

Enjoy building with ADK! 🚀
