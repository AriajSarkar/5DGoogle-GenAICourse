# 🤖 Google ADK Course - Build AI Agents from Scratch

**Welcome!** Learn to build powerful AI agents using Google's Agent Development Kit (ADK). This hands-on course takes you from basics to building sophisticated multi-agent systems.

---

## 🎯 What You'll Learn

- ✅ Build AI agents that can **think, act, and use tools**
- ✅ Create **custom tools** for your agents
- ✅ Integrate **Google Search** and other APIs
- ✅ Design **multi-agent workflows** (Sequential, Parallel, Loop, Coordinator patterns)
- ✅ **Production-ready** agent systems

---

## 📖 Course Modules

### Day 1a: From Prompt to Action
**Build your first AI agent!**

Learn the fundamentals: what agents are, how to create them, and how to give them superpowers with tools.

**Topics:**
- What are AI agents vs. simple LLMs
- Creating basic agents with ADK
- Custom Python function tools
- Built-in Google Search tool
- Multi-turn conversations
- Combining multiple tools

**📂 [Start Day 1a →](Day1/1a-from-prompt-to-action/)**

---

### Day 1b: Agent Architectures
**Build teams of AI agents!**

Master multi-agent systems and workflow patterns for complex tasks.

**Topics:**
- Why multi-agent > monolithic systems
- **LLM-Based Coordinator** - Dynamic routing
- **Sequential Pattern** - Assembly line workflows
- **Parallel Pattern** - Concurrent execution
- **Loop Pattern** - Iterative refinement
- Choosing the right pattern

**📂 [Start Day 1b →](Day1/1b-agent-architectures/)**

---

## ⚡ Quick Start

### 1. Prerequisites

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Google API Key** ([Get free key](https://aistudio.google.com/app/apikey))

### 2. Setup (5 minutes)

```powershell
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. ⚠️ IMPORTANT: Install this project (makes utils/ importable)
pip install -e .

# 5. Configure environment variables
copy .env.example .env  # Then edit .env with your keys
```

**⚠️ CRITICAL STEP:** The `pip install -e .` command is **required** to avoid "No module named 'utils'" errors!

**Required in `.env` file:**
```bash
GOOGLE_API_KEY=AIza...your-key-here
GEMINI_TEXT_MODEL=gemini-2.5-flash-lite
GEMINI_MULTIMODAL_MODEL=gemini-2.0-flash-preview-image-generation
GEMINI_PRO_MODEL=gemini-2.5-pro
```

### 3. Run Your First Agent!

```powershell
# Make sure virtual environment is activated!
adk run Day1/1a-from-prompt-to-action/basic_agent
```

You should see an interactive chat interface! Type your questions and the agent will respond. 🎉

**Alternative:** Run the standalone Python script:
```powershell
python Day1/1a-from-prompt-to-action/01_basic_agent.py
```

**Need detailed setup help?** → See [SETUP.md](SETUP.md)  
**Learn about `adk run`** → See [ADK_USAGE_GUIDE.md](ADK_USAGE_GUIDE.md)

---

## 📂 Repository Structure

```
Google-Course/
│
├── 📄 SETUP.md                    ← Complete setup guide
├── 📄 QUICK_REFERENCE.md          ← Command cheat sheet
├── 📄 .env.example                ← API key template
├── 📄 requirements.txt            ← All dependencies
│
├── 📁 Day1/
│   │
│   ├── 📁 1a-from-prompt-to-action/
│   │   ├── README.md              ← Module guide
│   │   ├── 01_basic_agent.py      ← Start here!
│   │   ├── 02_agent_with_custom_tool.py
│   │   ├── 03_agent_with_google_search.py
│   │   ├── 04_multi_tool_agent.py
│   │   └── 05_interactive_agent.py
│   │
│   └── 📁 1b-agent-architectures/
│       ├── README.md              ← Module guide
│       ├── 01_llm_coordinator_pattern.py
│       ├── 02_sequential_pattern.py
│       ├── 03_parallel_pattern.py
│       ├── 04_loop_pattern.py
│       └── 05_pattern_comparison.py
│
└── 📁 .venv/                      ← Virtual environment
```

---

## 🎓 Learning Path

### For Complete Beginners:

```
START HERE
    ↓
1. Read SETUP.md (setup everything)
    ↓
2. Day 1a/README.md (concepts)
    ↓
3. Run Day 1a scripts (01 → 05)
    ↓
4. Day 1b/README.md (multi-agent)
    ↓
5. Run Day 1b scripts (01 → 05)
    ↓
BUILD YOUR OWN AGENT! 🚀
```

### Quick Learners:

1. Run setup commands above
2. Run scripts in each Day folder (01-05)
3. Read comments in code to understand
4. Check QUICK_REFERENCE.md for commands

---

## 🛠️ Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| **google-adk** | 1.18.0+ | Agent framework |
| **Python** | 3.12+ | Programming language |
| **gemini-2.5-flash** | Latest | AI model (fast & supports tools!) |
| **pytz** | 2025.2 | Timezone support |

**Why gemini-2.5-flash?**
- ⚡ Fastest Gemini model
- ✅ Full tool/function calling support
- 🎯 Perfect for learning & production

---

## 📝 What Makes This Course Special

✅ **Hands-On** - Every concept has runnable code  
✅ **Progressive** - Start simple, build to advanced  
✅ **Production-Ready** - Learn patterns used in real systems  
✅ **Well-Documented** - Clear comments and guides  
✅ **Modular** - Each script is self-contained  
✅ **Modern** - Uses latest ADK features & best practices

---

## 🆘 Common Issues

### "Module not found: google.adk"

```powershell
# Activate virtual environment first!
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "API key not found"

```powershell
# Set the environment variable:
$env:GOOGLE_API_KEY="your-key-here"

# Or create .env file:
copy .env.example .env
# Then edit .env and add your key
```

### "Cannot activate script"

```powershell
# Windows: Set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**More troubleshooting:** See [SETUP.md](SETUP.md)

---

## 📚 Additional Resources

- **[SETUP.md](SETUP.md)** - Complete setup guide with troubleshooting
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - All commands and code templates
- **[Google AI Studio](https://aistudio.google.com/)** - Get your free API key
- **[ADK GitHub](https://github.com/google/adk)** - Official ADK repository

---

## 🎯 Ready to Start?

**Complete Beginner?**
1. Read [SETUP.md](SETUP.md) first
2. Then start with [Day 1a](Day1/1a-from-prompt-to-action/README.md)

**Have Python & API key?**
1. Run setup commands above
2. Jump to [Day 1a/01_basic_agent.py](Day1/1a-from-prompt-to-action/01_basic_agent.py)

**Just want quick reference?**
→ See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 🌟 What Students Build

By the end of this course, you'll be able to build:

- 🔍 **Research Agents** - That can search and analyze information
- 💬 **Chat Assistants** - With tool-calling capabilities
- 🏭 **Workflow Pipelines** - Multi-agent assembly lines
- 🔄 **Iterative Refiners** - Loop patterns for quality
- 🎯 **Smart Routers** - LLM-based coordinators

---

**Questions? Issues? Check the troubleshooting sections in SETUP.md!**

**Ready to build AI agents? Let's go!** 🚀

---

<sub>**Last Updated:** November 2025 | **ADK Version:** 1.18.0+ | **Model:** gemini-2.5-flash</sub>
