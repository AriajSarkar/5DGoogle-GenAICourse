# Day 3b: Agent Memory - Memory Management Part 2

## 🎯 Learning Objectives

By the end of this module, you will:

- ✅ Understand the difference between Sessions (short-term) and Memory (long-term)
- ✅ Initialize MemoryService and integrate with agents
- ✅ Transfer session data to persistent memory storage
- ✅ Search and retrieve memories across conversations
- ✅ Automate memory storage with callbacks
- ✅ Understand memory consolidation concepts

---

## 📚 Core Concepts

### What is Memory?

**Memory** is a searchable, long-term knowledge store that persists **across multiple conversations**.

| Aspect | Session | Memory |
|--------|---------|--------|
| **Scope** | Single conversation | All conversations |
| **Lifespan** | Current chat thread | Persistent |
| **Analogy** | Application state | Database |
| **Size** | Full conversation history | Extracted key facts |
| **Search** | Chronological playback | Semantic/keyword search |

### When to Use What?

**Session (Short-term):**
```
User: "My favorite color is blue"
Agent: "Great, I'll remember that!"
User: "What's my favorite color?"  ← Session remembers
Agent: "Blue"

[New conversation]
User: "What's my favorite color?"  ← Session FORGETS
Agent: "I don't know"
```

**Memory (Long-term):**
```
User: "My favorite color is blue"
→ Saved to memory

[Days later, new conversation]
User: "What's my favorite color?"  ← Memory RECALLS
Agent: "Blue"
```

---

## 🧠 Three-Step Memory Workflow

```
1. INITIALIZE
   └── Create MemoryService + provide to Runner

2. INGEST
   └── Transfer session data: add_session_to_memory()

3. RETRIEVE
   └── Search memories: load_memory or preload_memory tools
```

---

## 📂 Module Structure

```
3b-agent-memory/
├── README.md                          # This file
├── basic_memory/                      # ADK app: Initialize + manual memory
├── auto_memory/                       # ADK app: Automated memory with callbacks
├── memory_search/                     # ADK app: Memory retrieval patterns
├── 01_basic_memory.py                # Standalone reference
├── 02_auto_memory.py                 # Standalone reference
└── 03_memory_consolidation.py        # Standalone reference (concept demo)
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

```bash
GOOGLE_API_KEY=AIza...
GEMINI_TEXT_MODEL=gemini-2.5-flash-lite
GEMINI_MULTIMODAL_MODEL=gemini-2.0-flash-preview-image-generation
GEMINI_PRO_MODEL=gemini-2.5-pro
```

---

## 📝 Examples Overview

### 1️⃣ Basic Memory (`basic_memory/`)

**What it teaches:**
- Initializing InMemoryMemoryService
- Manual memory ingestion
- Cross-session memory retrieval
- load_memory vs preload_memory

**Key concepts:**

```python
# Step 1: Initialize
memory_service = InMemoryMemoryService()
runner = Runner(
    agent=agent,
    session_service=session_service,
    memory_service=memory_service,  # Both services!
)

# Step 2: Ingest (manual)
session = await session_service.get_session(...)
await memory_service.add_session_to_memory(session)

# Step 3: Retrieve (via agent tool)
agent = LlmAgent(
    tools=[load_memory],  # Agent can search memory
    ...
)
```

**Memory retrieval tools:**

| Tool | Behavior | Use Case |
|------|----------|----------|
| **load_memory** | Reactive - agent decides when to search | Efficient, agent controls |
| **preload_memory** | Proactive - always searches | Guaranteed context, less efficient |

**Run it:**
```powershell
adk run Day3/3b-agent-memory/basic_memory
```

---

### 2️⃣ Automated Memory (`auto_memory/`)

**What it teaches:**
- Using callbacks for automatic memory saving
- Combining callbacks with preload_memory
- Zero-manual-intervention memory systems

**The problem:**
```python
# Manual memory (tedious!)
await run_session(runner, "My birthday is March 15", "conv-1")
session = await session_service.get_session(...)
await memory_service.add_session_to_memory(session)  # Manual!

await run_session(runner, "I like pizza", "conv-2")
session = await session_service.get_session(...)
await memory_service.add_session_to_memory(session)  # Manual again!
```

**The solution:**
```python
# Automatic memory with callbacks
async def auto_save_to_memory(callback_context):
    """Saves session to memory after EVERY agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

agent = LlmAgent(
    tools=[preload_memory],              # Auto-retrieve
    after_agent_callback=auto_save_to_memory,  # Auto-save
    ...
)

# Now this happens automatically:
await run_session(runner, "My birthday is March 15", "conv-1")  # ← Saved!
await run_session(runner, "I like pizza", "conv-2")             # ← Saved!
```

**Callback types:**

```python
# Save after each turn (common)
after_agent_callback=auto_save_to_memory

# Other callback options:
before_agent_callback     # Before agent processes
before_tool_callback      # Before tool calls
after_tool_callback       # After tool execution
on_model_error_callback   # On LLM errors
```

**Run it:**
```powershell
adk run Day3/3b-agent-memory/auto_memory
```

---

### 3️⃣ Memory Search Patterns (`memory_search/`)

**What it teaches:**
- Direct memory search in code
- Keyword matching (InMemoryMemoryService)
- Debugging memory contents

**Manual search API:**
```python
# Search memories programmatically
search_response = await memory_service.search_memory(
    app_name="MyApp",
    user_id="user-123",
    query="What is the user's favorite color?",
)

print(f"Found {len(search_response.memories)} memories")
for memory in search_response.memories:
    print(f"  [{memory.author}]: {memory.content.parts[0].text}")
```

**InMemoryMemoryService search behavior:**
```python
# Stored: "My favorite color is blue-green"

# ✅ Matches (keyword present)
query="favorite color"
query="blue-green"
query="color is blue"

# ❌ No match (keywords missing)
query="preferred hue"  # Different words
query="what shade"     # Synonym not recognized
```

**Run it:**
```powershell
adk run Day3/3b-agent-memory/memory_search
```

---

## 🔑 Key Patterns

### Complete Memory Integration

```python
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory, preload_memory

# 1. Initialize services
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

# 2. Create agent with memory tools
agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    tools=[load_memory],  # or preload_memory
    instruction="Use load_memory to recall past conversations",
)

# 3. Create runner with BOTH services
runner = Runner(
    agent=agent,
    app_name="MyApp",
    session_service=session_service,
    memory_service=memory_service,  # Required for memory!
)

# 4. Have conversation
await run_session(runner, "My name is Sam", "conv-1")

# 5. Save to memory (manual)
session = await session_service.get_session(
    app_name="MyApp",
    user_id="user-123",
    session_id="conv-1",
)
await memory_service.add_session_to_memory(session)

# 6. Retrieve in new session
await run_session(runner, "What's my name?", "conv-2")
# Agent uses load_memory → finds "Sam"
```

### Automated Memory with Callbacks

```python
# Define callback
async def auto_save_to_memory(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

# Create agent with callback
agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    tools=[preload_memory],
    after_agent_callback=auto_save_to_memory,  # Automatic!
)

# Now every conversation is automatically saved
await run_session(runner, "My birthday is March 15", "conv-1")  # Auto-saved
await run_session(runner, "When is my birthday?", "conv-2")     # Auto-retrieved
```

---

## 🎯 Best Practices

### 1. Choose the Right Memory Tool

**Use `load_memory` (reactive) when:**
```python
# Agent handles occasional memory lookups
# Saves tokens when memory not needed
agent = LlmAgent(
    tools=[load_memory],
    instruction="Use load_memory when you need past context",
)
```

**Use `preload_memory` (proactive) when:**
```python
# Memory ALWAYS needed (customer support, personalization)
# Willing to pay token cost for guaranteed context
agent = LlmAgent(
    tools=[preload_memory],  # Loads memory every turn
)
```

### 2. When to Save to Memory

**After every turn (real-time):**
```python
after_agent_callback=auto_save_to_memory
# Use when: Live learning, immediate personalization
```

**End of conversation (batch):**
```python
# Manual call when session ends
await memory_service.add_session_to_memory(final_session)
# Use when: Reducing API calls, post-processing needed
```

**Periodic intervals:**
```python
# Timer-based background job
# Use when: Long-running conversations, cost optimization
```

### 3. Memory Service Selection

**Development (this notebook):**
```python
memory_service = InMemoryMemoryService()
# ✅ Fast, simple
# ❌ Keyword-only search, no persistence
```

**Production (Day 5):**
```python
memory_service = VertexAiMemoryBankService(...)
# ✅ Semantic search, consolidation, persistent
# ✅ Handles scale, reduces storage costs
```

---

## 🧩 Memory Consolidation (Conceptual)

### The Problem with Raw Storage

```
Session with 50 messages:
├── User: "My favorite color is blue-green"
├── Agent: "Great!"
├── User: "I also like purple"
├── Agent: "Noted"
├── User: "Actually, I prefer blue-green most"
├── Agent: "Understood"
└── User: "Thanks!"
    └── Agent: "You're welcome!"

→ Stores ALL 50 messages (10,000 tokens)
→ Search returns ALL messages
→ Agent must process 10,000 tokens
```

### After Consolidation

```
Extracted Memory:
└── "User's favorite color: blue-green"

→ Stores 1 concise fact (10 tokens)
→ Search returns 1 fact
→ Agent processes 10 tokens
```

### How Consolidation Works

```
1. Raw Session Events
   ↓
2. LLM analyzes conversation
   ↓
3. Extracts key facts
   ↓
4. Merges with existing memories (deduplication)
   ↓
5. Stores concise, actionable memories
```

**Example transformation:**

```python
# Input (verbose)
"I'm allergic to peanuts. I also can't eat tree nuts. 
 Basically anything with nuts is bad for me."

# Output (consolidated)
{
  "allergy": "peanuts, tree nuts",
  "severity": "avoid completely",
  "category": "food"
}
```

### Implementation

**InMemoryMemoryService (this notebook):**
```python
# NO consolidation - stores raw events
await memory_service.add_session_to_memory(session)
# Stores: Full conversation verbatim
```

**VertexAiMemoryBankService (Day 5):**
```python
# Automatic consolidation
await memory_service.add_session_to_memory(session)
# Stores: LLM-extracted key facts only
```

**Same API, different behavior!** You'll explore consolidation in Day 5.

---

## 🐛 Common Issues

### Issue 1: Memory Not Retrieved

```python
# ❌ Problem: Forgot to add memory tools
agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    # Missing: tools=[load_memory]
)

# ✅ Solution: Add memory tool
agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    tools=[load_memory],  # Now agent can search memory
)
```

### Issue 2: Memory Service Not Provided

```python
# ❌ Problem: Only session service provided
runner = Runner(
    agent=agent,
    session_service=session_service,
    # Missing: memory_service=memory_service
)

# ✅ Solution: Provide both services
runner = Runner(
    agent=agent,
    session_service=session_service,
    memory_service=memory_service,  # Required!
)
```

### Issue 3: Forgot to Save Session

```python
# ❌ Problem: Had conversation but forgot to save
await run_session(runner, "My name is Sam", "conv-1")
# Memory is empty! Never called add_session_to_memory()

# ✅ Solution: Manual save
session = await session_service.get_session(...)
await memory_service.add_session_to_memory(session)

# ✅ Better: Automatic with callback
after_agent_callback=auto_save_to_memory
```

### Issue 4: Keyword Search Not Matching

```python
# ❌ Problem: InMemoryMemoryService uses keyword matching
# Stored: "My favorite color is blue"
query="preferred hue"  # No match! (different words)

# ✅ Solution: Use exact keywords
query="favorite color"  # Match!

# ✅ Better: Use semantic search (Day 5)
# VertexAiMemoryBankService matches meaning, not just words
```

---

## 🔗 Related Documentation

- [ADK Memory Documentation](https://cloud.google.com/products/ai/agent-development-kit)
- [Vertex AI Memory Bank](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/memory)
- [Memory Consolidation Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/memory)
- [ADK Callbacks](https://cloud.google.com/products/ai/agent-development-kit)

---

## 🎓 Next Steps

Once you've mastered memory basics, move on to:

📂 **Day 4: Observability & Evaluation** - Monitor and improve agent performance

📂 **Day 5: Production Memory** - Vertex AI Memory Bank with semantic search and consolidation

---

## 📝 Quick Reference

```python
# Initialize Memory
memory_service = InMemoryMemoryService()
runner = Runner(agent, session_service, memory_service)

# Manual Save
session = await session_service.get_session(app, user, session_id)
await memory_service.add_session_to_memory(session)

# Automatic Save (callback)
async def auto_save(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

agent = LlmAgent(
    tools=[load_memory],              # or preload_memory
    after_agent_callback=auto_save,
)

# Manual Search
results = await memory_service.search_memory(app, user, query)
for memory in results.memories:
    print(memory.content.parts[0].text)
```

---

## 🆚 Sessions vs Memory

| Feature | Session | Memory |
|---------|---------|--------|
| **Scope** | Single conversation | All conversations |
| **Storage** | Full events | Extracted facts |
| **Retrieval** | Chronological | Searchable |
| **Lifespan** | Conversation duration | Persistent |
| **Use case** | Context in current chat | Long-term knowledge |

**Rule of thumb:**
- Session = "What did we just talk about?"
- Memory = "What have we ever talked about?"

---

**Authors:** Adapted from Google ADK Course materials
