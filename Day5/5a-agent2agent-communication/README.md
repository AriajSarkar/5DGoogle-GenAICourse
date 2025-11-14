# Day 5a: Agent2Agent (A2A) Communication

Welcome to Day 5a! This module teaches you how to build **multi-agent systems** where different agents can communicate and collaborate using the **Agent2Agent (A2A) Protocol**.

## 📚 Overview

### The Problem
As you build complex AI systems, you'll find that:
- A single agent can't do everything - specialized agents for different domains work better
- You need agents to collaborate - customer support needs product data, inventory needs order info
- Different teams build different agents - you want to integrate agents from external vendors
- Agents may use different languages/frameworks - you need a standard communication protocol

### The Solution: A2A Protocol
The **Agent2Agent (A2A) Protocol** is a standard that allows agents to:
- ✨ **Communicate over networks** - Agents can be on different machines
- ✨ **Use each other's capabilities** - One agent can call another agent like a tool
- ✨ **Work across frameworks** - Language/framework agnostic
- ✨ **Maintain formal contracts** - Agent cards describe capabilities

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- ✅ Understand when to use A2A vs local sub-agents
- ✅ Expose ADK agents via A2A using `to_a2a()`
- ✅ Consume remote agents using `RemoteA2aAgent`
- ✅ Work with agent cards (the "contract" between agents)
- ✅ Build production-ready multi-agent integrations

## 🏗️ Common A2A Architecture Patterns

The A2A protocol is particularly useful in three scenarios:

### When to choose A2A?

| Scenario | Description | Example |
|----------|-------------|---------|
| **Cross-Framework Integration** | ADK agent communicating with other agent frameworks | Python ADK agent ↔ LangChain agent |
| **Cross-Language Communication** | Python agent calling Java or Node.js agent | Python support agent ↔ Java inventory service |
| **Cross-Organization Boundaries** | Your internal agent integrating with external vendor services | Your e-commerce app ↔ Vendor's product catalog |

### A2A vs Local Sub-Agents: Decision Table

| Factor | Use A2A | Use Local Sub-Agents |
|--------|---------|----------------------|
| **Agent Location** | External service, different codebase | Same codebase, internal |
| **Ownership** | Different team/organization | Your team |
| **Network** | Agents on different machines | Same process/machine |
| **Performance** | Network latency acceptable | Need low latency |
| **Language/Framework** | Cross-language/framework needed | Same language |
| **Contract** | Formal API contract required | Internal interface |
| **Example** | External vendor product catalog | Internal order processing steps |

## 📂 Module Structure

```
5a-agent2agent-communication/
├── product_catalog_server/         # ADK app: A2A server (vendor)
│   ├── __init__.py
│   └── agent.py                    # Product catalog agent to expose
├── customer_support_client/        # ADK app: A2A consumer (your company)
│   ├── __init__.py
│   └── agent.py                    # Support agent that consumes catalog
├── full_a2a_demo/                  # ADK app: Complete A2A ecosystem
│   ├── __init__.py
│   └── agent.py                    # Coordinator with A2A + local tools
├── 01_a2a_server.py                # Standalone: Expose agent via A2A
├── 02_a2a_client.py                # Standalone: Consume remote agent
├── 03_a2a_hybrid.py                # Standalone: Hybrid A2A + local tools
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites
1. **Install A2A dependencies:**
   ```powershell
   # Already included in requirements.txt
   pip install 'google-adk[a2a]'
   pip install uvicorn
   ```

2. **Activate virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Set API key (if not in .env):**
   ```powershell
   $env:GOOGLE_API_KEY="your-api-key"
   ```

### Running the Examples

#### Option 1: ADK Apps (Recommended for Learning)

**Step 1: Start Product Catalog Server**
```powershell
# Terminal 1: Start the A2A server
python Day5/5a-agent2agent-communication/01_a2a_server.py

# Verify server is running:
curl http://localhost:8001/.well-known/agent-card.json
```

**Step 2: Run Customer Support Client**
```powershell
# Terminal 2: Run the consumer agent
adk run Day5/5a-agent2agent-communication/customer_support_client/

# Ask: "What's the price of iPhone 15 Pro?"
# The agent will communicate with the Product Catalog Server via A2A!
```

**Step 3: Try the Hybrid Demo**
```powershell
# With server still running, test hybrid architecture
python Day5/5a-agent2agent-communication/03_a2a_hybrid.py

# This demonstrates A2A (product catalog) + local tools (tax calc)
```

#### Option 2: Standalone Scripts (Complete Examples)

```powershell
# Test 1: Expose agent via A2A
python Day5/5a-agent2agent-communication/01_a2a_server.py

# Test 2: Consume remote agent (in another terminal)
python Day5/5a-agent2agent-communication/02_a2a_client.py

# Test 3: Hybrid architecture (A2A + local tools)
python Day5/5a-agent2agent-communication/03_a2a_hybrid.py
```

## 📖 Examples Explained

### Example 1: Exposing an Agent via A2A (`01_a2a_server.py`)

**What it teaches:**
- How to convert any ADK agent to an A2A server using `to_a2a()`
- How agent cards are auto-generated
- How to run an A2A server with uvicorn

**Key concepts:**
```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Create agent
product_catalog_agent = LlmAgent(
    name="product_catalog_agent",
    tools=[get_product_info],
    ...
)

# Convert to A2A app (FastAPI/Starlette)
a2a_app = to_a2a(product_catalog_agent, port=8001)

# Agent card auto-generated at:
# http://localhost:8001/.well-known/agent-card.json
```

**What `to_a2a()` does:**
1. Wraps your agent in an A2A-compatible server (FastAPI/Starlette)
2. Auto-generates an agent card describing capabilities
3. Serves the agent card at `/.well-known/agent-card.json` (standard A2A path)
4. Handles all A2A protocol details (request/response formatting)

**Agent Card Example:**
```json
{
  "name": "product_catalog_agent",
  "description": "External vendor's product catalog agent",
  "url": "http://localhost:8001",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "name": "get_product_info",
      "description": "Get product information for a given product",
      ...
    }
  ]
}
```

### Example 2: Consuming a Remote Agent (`02_a2a_client.py`)

**What it teaches:**
- How to use `RemoteA2aAgent` to consume an A2A server
- How to use remote agents as sub-agents
- How ADK handles A2A protocol communication transparently

**Key concepts:**
```python
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

# Create remote agent proxy (client-side)
remote_catalog = RemoteA2aAgent(
    name="product_catalog_agent",
    description="Remote product catalog from vendor",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

# Use remote agent as a sub-agent (just like local!)
customer_support_agent = LlmAgent(
    sub_agents=[remote_catalog],  # Transparent A2A communication!
    ...
)
```

**What happens behind the scenes:**
1. Customer asks Support Agent a question
2. Support Agent realizes it needs product info
3. Support Agent calls `remote_catalog` (RemoteA2aAgent)
4. ADK sends HTTP POST to `http://localhost:8001/tasks`
5. Product Catalog Agent processes request and responds
6. RemoteA2aAgent receives response and passes to Support Agent
7. Support Agent formulates final answer

**All of this is TRANSPARENT** - Support Agent doesn't know catalog is remote!

### Example 3: Hybrid Architecture (`03_a2a_hybrid.py`)

**What it teaches:**
- When to use A2A vs local tools
- How to combine remote A2A agents with local tools
- Real-world architecture decisions

**Architecture:**
```
E-Commerce Coordinator Agent
    ├── RemoteA2aAgent: Product Catalog (A2A)
    │   ├── Why A2A: External vendor, different org
    │   └── Provides: Product info, pricing, availability
    └── Local Tool: calculate_tax()
        ├── Why Local: Simple calc, internal logic
        └── Provides: Sales tax calculation
```

**Key concepts:**
```python
# Remote A2A agent for external product data
remote_catalog = RemoteA2aAgent(
    agent_card="http://localhost:8001/.well-known/agent-card.json"
)

# Local tool for internal tax calculation
def calculate_tax(state: str, price: float) -> dict:
    """Fast local calculation - no network call needed."""
    ...

# Coordinator uses BOTH
coordinator = LlmAgent(
    sub_agents=[remote_catalog],  # A2A for external data
    tools=[calculate_tax],        # Local for fast calculations
    ...
)
```

**Decision rationale:**
- **Product Catalog → A2A:**
  - Owned by external vendor (different organization)
  - Formal API contract needed
  - Network latency acceptable
  
- **Tax Calculation → Local Tool:**
  - Simple calculation (no external dependency)
  - Fast execution (no network call)
  - Internal business logic

## 🔍 Key Concepts

### 1. Agent Cards
An **agent card** is a JSON document that serves as a "business card" for your agent.

**What it includes:**
- Agent name, description, and version
- Skills (your tools/functions become "skills")
- Protocol version and endpoints
- Input/output modes

**Standard location:** `/.well-known/agent-card.json`

**Why it matters:**
- Tells other agents what your agent can do
- Defines the "contract" between agents
- Enables automatic discovery of capabilities

### 2. A2A Protocol Endpoints

**Agent Card Endpoint:**
```
GET http://localhost:8001/.well-known/agent-card.json
```
Returns the agent's capabilities (agent card).

**Task Endpoint:**
```
POST http://localhost:8001/tasks
```
Sends a task/query to the agent. ADK handles this automatically when you use `RemoteA2aAgent`.

### 3. `to_a2a()` Function

**Purpose:** Converts any ADK agent into an A2A-compatible server.

**What it does:**
1. Wraps agent in FastAPI/Starlette app
2. Auto-generates agent card from agent definition
3. Serves agent card at standard path
4. Handles A2A protocol (request/response formatting)

**Usage:**
```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a

a2a_app = to_a2a(my_agent, port=8001)
```

### 4. `RemoteA2aAgent` Class

**Purpose:** Client-side proxy for consuming remote A2A agents.

**What it does:**
1. Reads remote agent's card from `/.well-known/agent-card.json`
2. Translates sub-agent calls into A2A protocol requests
3. Sends HTTP POST to `/tasks` endpoint
4. Handles protocol details transparently

**Usage:**
```python
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

remote_agent = RemoteA2aAgent(
    name="remote_agent_name",
    agent_card=f"http://remote-server:8001{AGENT_CARD_WELL_KNOWN_PATH}"
)

# Use like any sub-agent
my_agent = LlmAgent(sub_agents=[remote_agent], ...)
```

## 🛠️ Troubleshooting

### Server not starting
```powershell
# Check if port 8001 is already in use
netstat -ano | findstr :8001

# Kill process if needed
taskkill /PID <PID> /F

# Restart server
python Day5/5a-agent2agent-communication/01_a2a_server.py
```

### Cannot connect to remote agent
```powershell
# Verify server is running
curl http://localhost:8001/.well-known/agent-card.json

# Should return JSON agent card
# If not, start server first
```

### Import errors
```powershell
# Verify A2A dependencies installed
pip list | Select-String "google-adk"
pip list | Select-String "uvicorn"

# Reinstall if needed
pip install 'google-adk[a2a]'
pip install uvicorn
```

### "ModuleNotFoundError: No module named 'utils'"
```powershell
# Install project as editable package
pip install -e .

# This makes utils/ importable everywhere
```

## 📚 Additional Resources

### ADK Documentation
- [Introduction to A2A in ADK](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/a2a)
- [Exposing Agents Quickstart](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/a2a/exposing-agents)
- [Consuming Agents Quickstart](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/a2a/consuming-agents)

### A2A Protocol
- [Official A2A Protocol Website](https://www.google.com/agentspace)
- [A2A Protocol Specification](https://www.google.com/agentspace/docs)

### Production Deployment
- [Deploy ADK Agents to Cloud Run](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-cloud-run)
- [Deploy to Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-agent-engine)
- [Deploy to GKE](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-gke)

## 💡 Best Practices

### When to Use A2A
✅ **Use A2A when:**
- Agent owned by different team/organization
- Agent runs on different infrastructure
- Formal API contract needed
- Cross-language/framework integration required
- Network latency acceptable

❌ **Use local sub-agents when:**
- Same codebase, internal to your team
- Same process/machine
- Need low latency
- No formal contract needed
- Internal interface

### Production Considerations
- **Authentication:** Add API keys or OAuth to A2A endpoints
- **Rate Limiting:** Protect your A2A server from abuse
- **Error Handling:** Handle network failures gracefully
- **Monitoring:** Track A2A request/response metrics
- **Versioning:** Use agent card version field for breaking changes

### Performance Tips
- **Keep fast operations local:** Don't use A2A for simple calculations
- **Batch requests:** Combine multiple A2A calls when possible
- **Cache agent cards:** Don't fetch agent card on every request
- **Use timeouts:** Set reasonable timeouts for A2A calls

## 🎓 What's Next?

Now that you understand A2A communication, proceed to **Day 5b: Agent Deployment** to learn how to deploy your agents to production!

**Topics in Day 5b:**
- Deploying to Vertex AI Agent Engine
- Deploying to Cloud Run
- Adding Memory Bank for long-term memory
- Cost management and cleanup

---

**Questions?** Check the [main course README](../../README.md) or ask on the [Kaggle Discord](https://discord.gg/kaggle).
