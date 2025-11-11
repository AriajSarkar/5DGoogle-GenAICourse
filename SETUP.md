# 🚀 Google ADK Course - Complete Setup Guide

**Welcome!** This guide will help you set up everything you need to start building AI agents with Google's Agent Development Kit (ADK).

---

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.12+** installed ([Download here](https://www.python.org/downloads/))
- **Git** (optional, for cloning)
- A **Google AI Studio API Key** (we'll get this below)

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Get Your Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy your API key (starts with `AIza...`)

### Step 2: Set Up Python Environment

Open your terminal/PowerShell in the `Google-Course` folder and run:

```powershell
# Create virtual environment
python -m venv .venv

# Activate it (Windows)
.\.venv\Scripts\Activate.ps1

# Activate it (Linux/Mac)
source .venv/bin/activate
```

**Troubleshooting (Windows):** If you get "execution policy" error:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
# Install required packages
pip install -r requirements.txt

# Install this project (so utils/ is importable)
pip install -e .
```

This installs:
- `google-adk` - The Agent Development Kit
- `python-dotenv` - Auto-loads .env file
- `pytz` - Timezone support for examples
- **Your project** - Makes `utils/` importable (fixes "No module named 'utils'" errors)

### Step 4: Configure Your API Key

**Option A: Environment Variable (Temporary)**
```powershell
# Windows PowerShell
$env:GOOGLE_API_KEY="your-api-key-here"

# Linux/Mac
export GOOGLE_API_KEY="your-api-key-here"
```

**Option B: .env File (Recommended)**
```powershell
# Copy the example file
copy .env.example .env

# Edit .env and add your keys:
# GOOGLE_API_KEY=AIza...your-key-here
# GEMINI_TEXT_MODEL=gemini-2.5-flash-lite
# GEMINI_MULTIMODAL_MODEL=gemini-2.0-flash-preview-image-generation
# GEMINI_PRO_MODEL=gemini-2.5-pro
```

**⚠️ Required Variables:**
- `GOOGLE_API_KEY` - Your API key from Google AI Studio
- `GEMINI_TEXT_MODEL` - Model for text agents (11/12 agents)
- `GEMINI_MULTIMODAL_MODEL` - Model for image generation agents
- `GEMINI_PRO_MODEL` - Premium model option

### Step 5: Test Your Setup

```powershell
# Make sure virtual environment is activated!
.\.venv\Scripts\Activate.ps1

# Run a test script
python Day1/1a-from-prompt-to-action/01_basic_agent.py
```

If you see a response from the agent, **you're all set!** 🎉

---

## 📚 What's Included

```
Google-Course/
│
├── .env                          ← Your API key (create from .env.example)
├── .env.example                  ← Template
├── requirements.txt              ← All dependencies
├── SETUP.md                      ← This file
├── README.md                     ← Course overview
│
├── Day1/
│   ├── 1a-from-prompt-to-action/
│   │   ├── README.md             ← Complete Day 1a guide
│   │   ├── 01_basic_agent.py     ← Start here!
│   │   ├── 02_agent_with_custom_tool.py
│   │   ├── 03_agent_with_google_search.py
│   │   ├── 04_multi_tool_agent.py
│   │   └── 05_interactive_agent.py
│   │
│   └── 1b-agent-architectures/
│       ├── README.md             ← Complete Day 1b guide
│       ├── 01_llm_coordinator_pattern.py
│       ├── 02_sequential_pattern.py
│       ├── 03_parallel_pattern.py
│       ├── 04_loop_pattern.py
│       └── 05_pattern_comparison.py
│
└── QUICK_REFERENCE.md            ← Handy cheat sheet
```

---

## 🎓 Learning Path

### Beginner? Start Here:

1. **Read:** Main `README.md` for overview
2. **Run:** Day 1a scripts in order (01 → 05)
3. **Learn:** Multi-agent patterns in Day 1b
4. **Build:** Your own agent system!

### Each Day Folder Contains:

- **README.md** - Complete guide for that module
- **01-05 scripts** - Progressive examples
- **VISUAL_GUIDE.md** - Diagrams and decision trees (where applicable)

---

## 🔧 Common Setup Issues

### Issue: "Command not found: python"

**Solution:** Try `python3` instead of `python`, or install Python from [python.org](https://www.python.org/downloads/)

### Issue: "Cannot activate virtual environment"

**Windows:**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### Issue: "API key not found"

**Solution:** Make sure you've either:
1. Set the environment variable: `$env:GOOGLE_API_KEY="your-key"`
2. Created `.env` file with `GOOGLE_API_KEY=your-key`

### Issue: "Module not found: google.adk"

**Solution:** Activate virtual environment first, then install:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "Model not supported"

**Solution:** We use `gemini-2.5-flash` which now supports tools! Make sure you're using the latest version:
```powershell
pip install --upgrade google-adk
```

---

## 🌟 Models Available

| Model | Speed | Tools? | Best For |
|-------|-------|--------|----------|
| **gemini-2.5-flash** | ⚡ Very Fast | ✅ Yes | **RECOMMENDED** - Fast & supports all features |
| gemini-1.5-flash | ⚡ Fast | ✅ Yes | Alternative if 2.5 unavailable |

**We use `gemini-2.5-flash` throughout this course!**

---

## 📖 Next Steps

After setup, here's your learning journey:

### Day 1a: From Prompt to Action
**What you'll learn:**
- What are AI agents
- Creating basic agents
- Adding custom tools
- Using Google Search
- Multi-turn conversations

**Start:** `Day1/1a-from-prompt-to-action/README.md`

### Day 1b: Agent Architectures
**What you'll learn:**
- Why multi-agent systems
- 4 workflow patterns
- When to use each pattern
- Building agent teams

**Start:** `Day1/1b-agent-architectures/README.md`

---

## 💡 Tips for Success

1. **Always activate the virtual environment** before running scripts:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Run scripts in order** (01 → 05) for best learning

3. **Read the comments** in each script - they explain what's happening

4. **Experiment!** Modify the scripts, try different prompts, break things and fix them

5. **Check QUICK_REFERENCE.md** when you need a command reminder

---

## 🆘 Getting Help

**If you're stuck:**

1. Check the troubleshooting section above
2. Read the module README (`Day1/1a-from-prompt-to-action/README.md`)
3. Look at `QUICK_REFERENCE.md` for quick command reference
4. Make sure your virtual environment is activated
5. Verify your API key is set correctly

---

## ✅ Verification Checklist

Before starting the course, make sure:

- [ ] Python 3.12+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google API key obtained from AI Studio
- [ ] API key set (environment variable or .env file)
- [ ] Test script runs successfully

---

## 🎯 Ready to Start!

Everything is set up! Here's what to do now:

```powershell
# 1. Make sure you're in the virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Go to Day 1a
cd Day1/1a-from-prompt-to-action

# 3. Read the guide
# Open README.md in your editor

# 4. Run the first example
python 01_basic_agent.py
```

**Welcome to the world of AI agents!** 🤖✨

---

## 📚 Additional Resources

- **Google AI Studio:** https://aistudio.google.com/
- **ADK Documentation:** https://github.com/google/adk
- **Python Virtual Environments:** https://docs.python.org/3/tutorial/venv.html

---

**Last Updated:** November 2025  
**ADK Version:** 1.18.0+  
**Python Version:** 3.12+  
**Recommended Model:** gemini-2.5-flash
