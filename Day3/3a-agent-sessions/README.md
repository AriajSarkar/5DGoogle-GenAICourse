# Day 3a: Agent Sessions - Memory Management Part 1

## 🎯 Learning Objectives

By the end of this module, you will:

- ✅ Understand the difference between stateless LLMs and stateful agents
- ✅ Implement conversation history with Sessions and Events
- ✅ Use InMemorySessionService for development
- ✅ Persist sessions with DatabaseSessionService
- ✅ Implement Context Compaction to manage token costs
- ✅ Share data across conversation turns with Session State

---

## 📚 Core Concepts

### What is a Session?

A **Session** is a container for a single conversation thread. It encapsulates:

- **Events**: Chronological record of all interactions (user messages, agent responses, tool calls)
- **State**: A key-value store for sharing data across turns (like a global scratchpad)

**Key characteristics:**
- Sessions are **user-specific** (not shared between users)
- Sessions are **agent-specific** (each agent has its own session history)
- Sessions provide **short-term memory** for a single conversation

### Session Components

```
Session
├── Events (conversation history)
│   ├── User Input: "Hi, I'm Sam"
│   ├── Agent Response: "Hello Sam!"
│   ├── Tool Call: get_weather("London")
│   └── Tool Output: {"temp": 15, "conditions": "cloudy"}
│
└── State (shared data)
    ├── "user:name" → "Sam"
    ├── "user:country" → "Poland"
    └── "temp:preference" → "celsius"
```

### SessionService Types

| Service | Persistence | Best For | Storage |
|---------|-------------|----------|---------|
| **InMemorySessionService** | ❌ Lost on restart | Development, testing | RAM |
| **DatabaseSessionService** | ✅ Survives restarts | Self-hosted apps | SQLite/Postgres |
| **Agent Engine Sessions** | ✅ Fully managed | Production on GCP | Cloud |

---

## 📂 Module Structure

```
3a-agent-sessions/
├── README.md                           # This file
├── stateful_agent/                     # ADK app: Basic session management
├── persistent_sessions/                # ADK app: DatabaseSessionService
├── session_compaction/                 # ADK app: Context compaction
├── session_state_demo/                 # ADK app: Session State management
├── 01_stateful_agent.py               # Standalone reference
├── 02_persistent_sessions.py          # Standalone reference
└── 03_session_state.py                # Standalone reference
```

---

## 🚀 Getting Started

### Prerequisites

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Verify installation
pip list | Select-String "google-adk"
```

### Required Environment Variables

Ensure your `.env` file contains:

```bash
GOOGLE_API_KEY=AIza...
GEMINI_TEXT_MODEL=gemini-2.5-flash-lite
GEMINI_MULTIMODAL_MODEL=gemini-2.0-flash-preview-image-generation
GEMINI_PRO_MODEL=gemini-2.5-pro
```

---

## 📝 Examples Overview

### 1️⃣ Basic Stateful Agent (`stateful_agent/`)

**What it teaches:**
- Creating a session-aware agent
- Understanding InMemorySessionService
- Conversation continuity across turns

**Key concepts:**
```python
# Session enables context retention
session_service = InMemorySessionService()
runner = Runner(agent=agent, session_service=session_service)

# Conversation 1
"Hi, I'm Sam!"  # Agent learns name

# Conversation 2 (same session)
"What's my name?"  # Agent remembers: "Sam"
```

**Run it:**
```powershell
adk run Day3/3a-agent-sessions/stateful_agent
```

---

### 2️⃣ Persistent Sessions (`persistent_sessions/`)

**What it teaches:**
- Surviving application restarts
- Using SQLite for session storage
- Session isolation between users

**Key concepts:**
```python
# Persist sessions to database
db_url = "sqlite:///my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# Sessions survive restarts!
# Stop notebook → Restart → Sessions still exist
```

**Database schema:**
```sql
events table:
├── app_name      (e.g., "default")
├── session_id    (e.g., "user-123-conv-1")
├── author        (e.g., "user" or "agent_name")
└── content       (JSON: {"parts": [{"text": "..."}]})
```

**Run it:**
```powershell
adk run Day3/3a-agent-sessions/persistent_sessions
```

---

### 3️⃣ Context Compaction (`session_compaction/`)

**What it teaches:**
- Managing long conversation costs
- Automatic history summarization
- Balancing context vs. efficiency

**The problem:**
```
Turn 1: 100 tokens
Turn 2: 200 tokens
Turn 3: 300 tokens
Turn 4: 400 tokens
→ Total: 1000 tokens sent to LLM every turn!
```

**The solution:**
```python
from google.adk.apps.app import App, EventsCompactionConfig

app = App(
    name="research_app",
    root_agent=agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,  # Compact after 3 turns
        overlap_size=1,         # Keep 1 recent turn
    ),
)
```

**What happens:**
```
After Turn 3:
├── Turns 1-2: Summarized → "User asked about AI. Agent explained basics."
├── Turn 3: Kept in full (overlap_size=1)
└── Turn 4+: New conversations

→ Reduced from 1000 tokens to ~200 tokens!
```

**Run it:**
```powershell
adk run Day3/3a-agent-sessions/session_compaction
```

---

### 4️⃣ Session State Management (`session_state_demo/`)

**What it teaches:**
- Sharing structured data across turns
- Creating state-aware tools
- Understanding state scope levels

**Use case:**
Store user preferences once, access everywhere:

```python
def save_userinfo(tool_context: ToolContext, name: str, country: str):
    """Tool that writes to session state."""
    tool_context.state["user:name"] = name
    tool_context.state["user:country"] = country
    return {"status": "success"}

def retrieve_userinfo(tool_context: ToolContext):
    """Tool that reads from session state."""
    name = tool_context.state.get("user:name", "Unknown")
    country = tool_context.state.get("user:country", "Unknown")
    return {"name": name, "country": country}
```

**State scope prefixes:**
- `user:` → User-specific data (e.g., preferences)
- `app:` → Application-wide data
- `temp:` → Temporary data (cleared after session)

**Run it:**
```powershell
adk run Day3/3a-agent-sessions/session_state_demo
```

---

## 🔑 Key Patterns

### Session Creation Flow

```python
# 1. Initialize session service
session_service = InMemorySessionService()

# 2. Create agent
agent = LlmAgent(model=Gemini(model=get_text_model()), ...)

# 3. Create runner with session service
runner = Runner(
    agent=agent,
    app_name="MyApp",
    session_service=session_service,
)

# 4. Create/get session
session = await session_service.create_session(
    app_name="MyApp",
    user_id="user-123",
    session_id="conversation-1",
)

# 5. Run queries
async for event in runner.run_async(
    user_id="user-123",
    session_id=session.id,
    new_message=query,
):
    print(event.content.parts[0].text)
```

### Session State Access Pattern

```python
# In a tool function
def my_tool(tool_context: ToolContext, value: str):
    # Write to state
    tool_context.state["user:preference"] = value
    
    # Read from state
    existing = tool_context.state.get("user:preference", "default")
    
    return {"status": "success"}
```

---

## 🎯 Best Practices

### 1. Session Naming Convention

```python
# Good: Descriptive, unique session IDs
session_id = f"{user_id}-{conversation_type}-{timestamp}"
# Example: "user123-support-20250112"

# Bad: Generic IDs
session_id = "default"  # Sessions will conflict!
```

### 2. Choose the Right SessionService

**Development:**
```python
# Fast, disposable, no setup
session_service = InMemorySessionService()
```

**Self-hosted production:**
```python
# Persistent, full control
session_service = DatabaseSessionService(db_url="sqlite:///sessions.db")
```

**Enterprise (Day 5):**
```python
# Managed, scalable
session_service = AgentEngineSessionService(...)
```

### 3. Context Compaction Strategy

```python
# For short conversations (< 10 turns)
# Don't use compaction - overhead not worth it

# For medium conversations (10-50 turns)
EventsCompactionConfig(
    compaction_interval=10,  # Compact every 10 turns
    overlap_size=2,          # Keep recent 2 turns
)

# For long conversations (50+ turns)
EventsCompactionConfig(
    compaction_interval=5,   # Compact frequently
    overlap_size=1,          # Minimal overlap
)
```

### 4. Session State Organization

```python
# Good: Namespaced keys
state["user:name"] = "Sam"
state["user:preferences:theme"] = "dark"
state["app:version"] = "1.0"

# Bad: Flat keys
state["name"] = "Sam"  # Unclear scope
state["theme"] = "dark"  # Could conflict
```

---

## 🐛 Common Issues

### Issue 1: Session Not Found

```python
# ❌ Problem
session = await session_service.get_session(
    app_name="App1",
    user_id="user-123",
    session_id="conv-1",
)
# Error: Session not found

# ✅ Solution: Create session first
try:
    session = await session_service.create_session(...)
except:
    session = await session_service.get_session(...)
```

### Issue 2: InMemorySessionService Loses Data

```python
# ❌ Problem: Data lost after restart
session_service = InMemorySessionService()  # In RAM only!

# ✅ Solution: Use persistent storage
session_service = DatabaseSessionService(db_url="sqlite:///sessions.db")
```

### Issue 3: State Not Persisting Between Tools

```python
# ❌ Problem: Using local variable
def tool1(tool_context: ToolContext):
    my_var = "value"  # Lost after tool ends!

# ✅ Solution: Use session state
def tool1(tool_context: ToolContext):
    tool_context.state["my_var"] = "value"  # Persists!
```

---

## 🔗 Related Documentation

- [ADK Sessions Documentation](https://cloud.google.com/products/ai/agent-development-kit)
- [ADK Session State](https://cloud.google.com/products/ai/agent-development-kit)
- [Context Compaction Guide](https://cloud.google.com/products/ai/agent-development-kit)

---

## 🎓 Next Steps

Once you've mastered sessions, move on to:

📂 **[Day 3b: Agent Memory →](../3b-agent-memory/)** - Long-term knowledge storage across sessions

---

## 📝 Quick Reference

```python
# Session Creation
session_service = InMemorySessionService()
session = await session_service.create_session(app_name, user_id, session_id)

# Running Queries
async for event in runner.run_async(user_id, session_id, new_message):
    print(event.content.parts[0].text)

# Session State (in tools)
tool_context.state["key"] = value
value = tool_context.state.get("key", default)

# Context Compaction
app = App(
    root_agent=agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3,
        overlap_size=1,
    ),
)
```

---

**Authors:** Adapted from Google ADK Course materials
