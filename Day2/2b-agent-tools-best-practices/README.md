# Day 2b: Agent Tool Patterns and Best Practices

## Learning Objectives

Master advanced tool patterns for production-ready agents: external service integration via MCP and long-running operations with human approval workflows.

### Key Concepts Covered

1. **Model Context Protocol (MCP)** - Connect to external services without custom integration
2. **Long-Running Operations** - Build workflows that pause for human input
3. **Tool Pause/Resume** - Implement approval gates in agent workflows
4. **Resumable Apps** - Maintain state across conversation breaks
5. **Production Patterns** - Real-world agent architectures

## Prerequisites

- Completed Day 2a (Custom Agent Tools)
- Understanding of async/await in Python
- **Node.js/npm** installed (required for MCP server examples)
- Google API key configured in `.env`

## ADK Apps

### 1. MCP Image Agent (`mcp_image_agent/`)

Demonstrates Model Context Protocol integration with external MCP servers.

**What it does:**
- Connects to `@modelcontextprotocol/server-everything` MCP server
- Uses `getTinyImage` tool to generate test images
- Shows how to integrate community-built tools

**Prerequisites:**
```powershell
# Verify Node.js is installed
node --version  # Should be v16+
npm --version
```

**Platform Note (Windows):**
The agent automatically detects Windows and uses `npx.cmd` instead of `npx`. This fix is already applied in the code.

**Run:**
```powershell
adk run Day2/2b-agent-tools-best-practices/mcp_image_agent
```

**Try:**
- "Provide a sample tiny image"
- "Generate a test image"

**Note:** This uses a demo MCP server for educational purposes. In production, you'd use servers for:
- Google Maps
- GitHub
- Slack
- Databases
- File systems
- [More MCP Servers](https://modelcontextprotocol.io/examples)

### 2. Shipping Approval Agent (`shipping_approval_agent/`)

Demonstrates long-running operations with human-in-the-loop approval.

**What it does:**
- Auto-approves small orders (≤5 containers)
- Pauses for approval on large orders (>5 containers)
- Resumes workflow after human decision

**Architecture:**
```
User Request → Agent → Tool
                        ↓
                   Large order?
                   ↙         ↘
              Yes              No
               ↓                ↓
          PAUSE HERE      Auto-approve
          Wait for human       ↓
               ↓           Return result
          Get decision
               ↓
          RESUME HERE
          Complete order
```

**Run:**
```powershell
adk run Day2/2b-agent-tools-best-practices/shipping_approval_agent
```

**Try in CLI (auto-approve only):**
- Small order: "Ship 3 containers to Singapore" (auto-approves immediately)
- Small order: "Ship 5 containers to London" (auto-approves immediately)

**⚠️ Important CLI Limitation:**
The interactive CLI cannot handle the full pause/resume approval workflow. Large orders (>5 containers) will return "pending" status but cannot get human approval interactively.

**For Full Approval Workflow:**
Use programmatic Runner with workflow code (see reference script when created). The workflow must:
1. Detect `adk_request_confirmation` event
2. Get human approval decision (UI/command line)
3. Resume with same `invocation_id`

## Model Context Protocol (MCP)

### What is MCP?

MCP is an open standard that lets agents use community-built integrations. Instead of writing your own API clients, connect to existing MCP servers.

### Architecture

```
┌──────────────────┐
│   Your Agent     │
│   (MCP Client)   │
└────────┬─────────┘
         │ Standard MCP Protocol
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
    ▼         ▼        ▼        ▼
┌────────┐ ┌─────┐ ┌──────┐ ┌─────┐
│ GitHub │ │Slack│ │ Maps │ │ ... │
│ Server │ │ MCP │ │ MCP  │ │     │
└────────┘ └─────┘ └──────┘ └─────┘
```

### MCP Integration Workflow

1. **Choose MCP Server** - Find servers at modelcontextprotocol.io
2. **Create McpToolset** - Configure connection parameters
3. **Add to Agent** - Include in tools list
4. **Use Tools** - Agent automatically discovers and calls MCP tools

### Example: Kaggle MCP Server

```python
mcp_kaggle = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=['-y', 'mcp-remote', 'https://www.kaggle.com/mcp'],
        ),
        timeout=30,
    )
)

agent = LlmAgent(
    tools=[mcp_kaggle],
    instruction="Use Kaggle MCP to search datasets..."
)
```

**What it provides:**
- 📊 Search and download Kaggle datasets
- 📓 Access notebook metadata
- 🏆 Query competition information

### Why MCP?

✅ **No custom integration code** - Just connect and use
✅ **Community ecosystem** - Leverage existing work
✅ **Standardized interface** - All servers work the same way
✅ **Easy to scale** - Add new capabilities by adding servers

## Long-Running Operations (LRO)

### The Problem

Normal tool execution is immediate:
```
User asks → Agent calls tool → Tool returns → Agent responds
```

But what if you need human approval before completing?

### The Solution: Pause/Resume Pattern

```
User asks → Agent calls tool → Tool PAUSES → Wait for human
                                              ↓
Agent responds ← Tool completes ← Tool RESUMES ← Human approves
```

### When to Use LRO

💰 **Financial transactions** - Require approval for large transfers
🗑️ **Bulk operations** - Confirm before deleting 1000 records
📋 **Compliance checkpoints** - Regulatory approval needed
💸 **High-cost actions** - Confirm before spinning up 50 servers
⚠️ **Irreversible operations** - Double-check account deletions

### Key Components

#### 1. ToolContext Parameter

ADK automatically provides this to your tool:

```python
def place_shipping_order(
    num_containers: int,
    destination: str,
    tool_context: ToolContext  # ADK injects this
) -> dict:
    ...
```

**Capabilities:**
- `tool_context.request_confirmation()` - Request approval (pauses execution)
- `tool_context.tool_confirmation` - Check approval status (after resume)

#### 2. Three Execution Scenarios

**Scenario 1: Auto-approve (no pause)**
```python
if num_containers <= 5:
    return {"status": "approved", ...}
```

**Scenario 2: First call - Pause for approval**
```python
if not tool_context.tool_confirmation:
    tool_context.request_confirmation(
        hint="Large order - approve?",
        payload={"containers": num_containers}
    )
    return {"status": "pending", ...}
```

**Scenario 3: Resumed call - Handle decision**
```python
if tool_context.tool_confirmation.confirmed:
    return {"status": "approved", ...}
else:
    return {"status": "rejected", ...}
```

#### 3. Resumable App

Wrap your agent in an App with resumability:

```python
shipping_app = App(
    name="shipping_coordinator",
    root_agent=shipping_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)
```

**What it saves:**
- All conversation messages
- Which tool was called
- Tool parameters
- Exact pause point

#### 4. Workflow Code

Your application code must:

1. **Detect pause** - Check for `adk_request_confirmation` event
2. **Get decision** - Show UI, wait for user input
3. **Resume execution** - Call `run_async()` with same `invocation_id`

```python
# First call - starts execution
events = []
async for event in runner.run_async(session_id=sid, new_message=query):
    events.append(event)

# Check if paused
approval_info = check_for_approval(events)

if approval_info:
    # Get human decision (True/False)
    approved = get_user_decision()
    
    # Resume with same invocation_id (CRITICAL!)
    async for event in runner.run_async(
        session_id=sid,
        new_message=create_approval_response(approval_info, approved),
        invocation_id=approval_info["invocation_id"]  # Same ID = resume
    ):
        print_response(event)
```

### Technical Deep Dive: Events and Invocation IDs

**Events** - ADK creates events as the agent executes:
- Tool calls → `function_call` event
- Model responses → `text` event
- Tool results → `function_response` event
- **Approval requests → `adk_request_confirmation` event** (special!)

**Invocation ID** - Unique identifier for each execution:
```
User sends message
  ↓
ADK assigns invocation_id = "abc123"
  ↓
Tool pauses, creates adk_request_confirmation event
  ↓
You save invocation_id = "abc123"
  ↓
User approves
  ↓
You call run_async(invocation_id="abc123")  ← Same ID = resume!
  ↓
Tool continues from exact pause point
```

Without the same invocation_id, ADK starts a NEW execution instead of resuming!

## Comparison: Agent Tools vs Sub-Agents

| Pattern | Control Flow | Use Case |
|---------|-------------|----------|
| **Agent Tools** (AgentTool) | Agent A calls Agent B → B returns → A continues | Delegation (calculations, translations) |
| **Sub-Agents** (SequentialAgent) | Agent A → transfers control → Agent B takes over | Handoff (customer support tiers) |

In currency converter: We want results back, so we use **Agent Tools**.

## Production Patterns Summary

| Pattern | When to Use | Key ADK Components |
|---------|-------------|-------------------|
| **MCP Integration** | Connect to external standardized services without custom code | `McpToolset`, `StdioConnectionParams` |
| **Long-Running Operations** | Pause workflow for human approval or external events | `ToolContext`, `request_confirmation`, `App`, `ResumabilityConfig` |

## Common Issues

### MCP Server Won't Start

**Problem:** `npx` command not found
**Solution:** Install Node.js from nodejs.org

**Problem (Windows):** `OSError: [WinError 193] %1 is not a valid Win32 application`
**Solution:** Already fixed! The agent now uses `npx.cmd` on Windows automatically.
```python
import platform
npx_command = "npx.cmd" if platform.system() == "Windows" else "npx"
```

**Problem:** MCP server times out
**Solution:** Increase timeout in `StdioConnectionParams(timeout=60)`

### Approval Workflow Not Working

**Problem:** Agent starts new execution instead of resuming
**Solution:** Ensure you're passing the same `invocation_id`:
```python
async for event in runner.run_async(
    invocation_id=approval_info["invocation_id"]  # Must match!
):
    ...
```

**Problem:** Can't detect approval request in CLI
**Solution:** The ADK CLI (`adk run`) cannot handle interactive approval workflows. Use programmatic Runner with workflow code instead.

**Problem:** Can't test large order approvals
**Solution:** For learning the pattern in CLI, test small orders (≤5 containers) which auto-approve. For full workflow, use programmatic implementation with event handling.

### State Not Persisting

**Problem:** Agent forgets context after pause
**Solution:** Ensure `ResumabilityConfig(is_resumable=True)` is set:
```python
app = App(
    root_agent=agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)
```

## Comparison: Kaggle vs Our Implementation

| Aspect | Kaggle Version | Our Version |
|--------|---------------|-------------|
| Environment | Jupyter Notebook | ADK App |
| Model | gemini-2.5-flash-lite | gemini-2.5-flash |
| MCP Server | npx command inline | Configured in agent.py |
| Workflow | Inline async code | Reusable workflow functions |
| Approval UI | Simulated boolean | Production-ready with invocation tracking |

## Exercise: Build Image Generation with Approval

**Scenario:** Build an agent that generates images using MCP, but requires approval for bulk requests:

1. Single image (1): Auto-approve
2. Bulk request (>1): Pause and ask for approval

**Steps:**
1. Create agent with MCP image server
2. Add approval logic to tool
3. Wrap in resumable App
4. Build workflow to handle approvals

## Next Steps

Continue to **Day 3: State and Memory Management** to learn:
- Session management across conversations
- Context window optimization
- Memory strategies for long-running agents

## Learn More

- [ADK Documentation](https://googleapis.github.io/agent-developer-kit/)
- [MCP Tools Documentation](https://googleapis.github.io/agent-developer-kit/docs/tools/mcp-tools/)
- [Long-Running Operations Guide](https://googleapis.github.io/agent-developer-kit/docs/tools/long-running-tools/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [ADK App and Runner](https://googleapis.github.io/agent-developer-kit/docs/core-concepts/app-and-runner/)

---

**Authors:** Laxmi Harikumar (Kaggle Course), Adapted for ADK by Course Team
**License:** Apache 2.0
