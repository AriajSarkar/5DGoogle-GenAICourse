# Day 5b: Agent Deployment to Production

Welcome to Day 5b! This module teaches you how to deploy your ADK agents to production using **Vertex AI Agent Engine** and other cloud platforms.

## 📚 Overview

### The Problem
You've built an amazing AI agent. It works perfectly on your machine. But there's a challenge:

- Your agent only lives in your development environment
- When you stop your notebook/script, it stops working
- Your teammates can't access it
- Your users can't interact with it

**Solution:** Deploy your agent to production infrastructure!

### What is Agent Deployment?
Deploying an agent means:
- ✨ **Making it publicly accessible** - Users can interact with it 24/7
- ✨ **Auto-scaling** - Handles varying traffic automatically
- ✨ **Production-grade** - Logging, monitoring, error handling
- ✨ **Persistent** - Runs independently of your local machine

## 🎯 Learning Objectives

By the end of this module, you'll be able to:
- ✅ Deploy agents to Vertex AI Agent Engine using `adk deploy`
- ✅ Configure resources (CPU, memory, scaling)
- ✅ Add Memory Bank for long-term memory across sessions
- ✅ Test deployed agents via SDK
- ✅ Monitor and manage deployed agents
- ✅ Implement cost management and cleanup

## 🏗️ Deployment Options

ADK supports multiple deployment platforms:

| Platform | Best For | Complexity | Cost | Documentation |
|----------|----------|------------|------|---------------|
| **Agent Engine** | AI agents | Low | Pay per use | [Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-agent-engine) |
| **Cloud Run** | Demos, APIs | Very low | Very low | [Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-cloud-run) |
| **GKE** | Enterprise | High | Higher | [Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-gke) |

**This module focuses on Agent Engine** - the recommended platform for ADK agents.

## 📂 Module Structure

```
5b-agent-deployment/
├── weather_agent_deploy/            # ADK app: Production-ready agent
│   ├── __init__.py
│   ├── agent.py                     # Weather agent
│   ├── requirements.txt             # Dependencies
│   ├── .env                         # Cloud config
│   └── .agent_engine_config.json   # Resource limits
├── memory_enabled_agent/            # ADK app: Agent with Memory Bank
│   ├── __init__.py
│   ├── agent.py                     # Memory-enabled weather agent
│   ├── requirements.txt
│   ├── .env
│   └── .agent_engine_config.json
├── 01_deploy_to_agent_engine.py    # Standalone: Deployment guide
├── 02_memory_bank_integration.py   # Standalone: Memory Bank demo
├── 03_production_config.py         # Standalone: Configuration guide
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

#### 1. Google Cloud Account
- **Create account:** [console.cloud.google.com](https://console.cloud.google.com)
- **Free trial:** New users get $300 in free credits (90 days)
- **Billing required:** Even for free trial (credit card for verification)

#### 2. Enable Required APIs
Enable these APIs in [Google Cloud Console](https://console.cloud.google.com/apis/library):
- Vertex AI API
- Cloud Storage API
- Cloud Logging API
- Cloud Monitoring API

Quick link: [Enable APIs](https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com,storage-api.googleapis.com,logging.googleapis.com,monitoring.googleapis.com)

#### 3. Install gcloud CLI
```powershell
# Download from: https://cloud.google.com/sdk/install

# Authenticate
gcloud auth application-default login

# Set project
gcloud config set project your-project-id
```

### Running the Examples

#### Option 1: View Deployment Guide
```powershell
# Educational guide (no deployment)
python Day5/5b-agent-deployment/01_deploy_to_agent_engine.py
```

#### Option 2: Test Memory Bank Locally
```powershell
# Test Memory Bank integration without deploying
python Day5/5b-agent-deployment/02_memory_bank_integration.py
```

#### Option 3: View Configuration Guide
```powershell
# Learn production configuration patterns
python Day5/5b-agent-deployment/03_production_config.py
```

#### Option 4: Deploy to Agent Engine (Requires GCP)
```powershell
# Set your project ID
$env:GOOGLE_CLOUD_PROJECT="your-project-id"

# Deploy weather agent
adk deploy agent_engine Day5/5b-agent-deployment/weather_agent_deploy/ `
    --project=$env:GOOGLE_CLOUD_PROJECT `
    --region=us-west1

# ⏱️ Deployment takes 2-5 minutes
```

## 📖 Examples Explained

### Example 1: Deploy to Agent Engine (`01_deploy_to_agent_engine.py`)

**What it teaches:**
- Complete deployment workflow for Agent Engine
- Required configuration files
- `adk deploy` command usage
- Testing deployed agents
- Cleanup to avoid costs

**Key deployment files:**

```
weather_agent_deploy/
├── __init__.py                  # Exports root_agent
├── agent.py                     # Agent definition
├── requirements.txt             # google-adk
├── .env                         # GOOGLE_CLOUD_LOCATION, GOOGLE_GENAI_USE_VERTEXAI
└── .agent_engine_config.json   # Resource limits
```

**Deployment command:**
```powershell
adk deploy agent_engine weather_agent_deploy/ \
    --project=your-project-id \
    --region=us-west1
```

**What happens:**
1. ADK packages your agent code
2. Uploads to Agent Engine
3. Creates containerized deployment
4. Returns resource name: `projects/.../reasoningEngines/...`

**Testing deployed agent:**
```python
import vertexai
from vertexai import agent_engines

# Initialize
vertexai.init(project="your-project-id", location="us-west1")

# Get deployed agent
agents_list = list(agent_engines.list())
remote_agent = agents_list[0]

# Query agent
async for item in remote_agent.async_stream_query(
    message="What's the weather in Tokyo?",
    user_id="user_123"
):
    print(item)
```

**Cleanup (IMPORTANT):**
```python
# Delete agent to avoid costs
agent_engines.delete(resource_name=remote_agent.resource_name, force=True)
```

### Example 2: Memory Bank Integration (`02_memory_bank_integration.py`)

**What it teaches:**
- Difference between session memory and Memory Bank
- How to add long-term memory to agents
- PreloadMemoryTool for automatic memory retrieval
- After-agent callback for automatic memory saving
- Cross-session recall

**Key concepts:**

| Feature | Session Memory | Memory Bank |
|---------|----------------|-------------|
| **Scope** | Single conversation | All conversations |
| **Persistence** | Lost when session ends | Permanent |
| **Use case** | "What did I just say?" | "What's my favorite city?" |
| **Setup** | Auto-enabled | Requires configuration |

**Memory workflow:**
1. User sets preference: "I prefer Celsius" (Session 1)
2. After-agent callback saves to Memory Bank
3. Days later, user returns (Session 2)
4. PreloadMemoryTool loads relevant memories
5. Agent responds in Celsius automatically ✨

**Implementation:**
```python
from google.adk.tools import preload_memory

# Callback to save memories
async def auto_save_to_memory(callback_context):
    memory_service = callback_context._invocation_context.memory_service
    if memory_service:
        session = callback_context._invocation_context.session
        await memory_service.add_session_to_memory(session)

# Memory-enabled agent
agent = LlmAgent(
    tools=[preload_memory],              # Auto-loads memories
    after_agent_callback=auto_save_to_memory,  # Auto-saves
    ...
)
```

**Local testing (InMemoryMemoryService):**
```python
from google.adk.memory import InMemoryMemoryService

memory_service = InMemoryMemoryService()

runner = Runner(
    agent=agent,
    session_service=session_service,
    memory_service=memory_service,  # Enable Memory Bank
)
```

**Production (Vertex AI Memory Bank):**
When deployed to Agent Engine, Vertex AI Memory Bank is used automatically:
- LLM-powered consolidation (not just keyword matching)
- Semantic search (finds related memories)
- Auto-scaling (handles large memory databases)

### Example 3: Production Configuration (`03_production_config.py`)

**What it teaches:**
- Resource configuration for different workloads
- Environment variable management
- Model selection strategies
- Monitoring and observability setup
- Cost optimization

**Configuration scenarios:**

**Development/Testing:**
```json
{
  "min_instances": 0,
  "max_instances": 1,
  "resource_limits": {"cpu": "1", "memory": "1Gi"}
}
```
- Scales to zero when idle (minimal cost)
- Good for demos and learning
- Cold start latency acceptable

**Production (Low Traffic):**
```json
{
  "min_instances": 1,
  "max_instances": 3,
  "resource_limits": {"cpu": "2", "memory": "2Gi"}
}
```
- Always 1 instance running (no cold start)
- Auto-scales to 3 if needed
- Good for small production apps

**Production (High Traffic):**
```json
{
  "min_instances": 3,
  "max_instances": 10,
  "resource_limits": {"cpu": "4", "memory": "4Gi"}
}
```
- Always 3 instances running
- Scales up to 10 for traffic spikes
- Low latency, handles high load

## 🔍 Key Concepts

### 1. Agent Engine Configuration

**File: `.agent_engine_config.json`**

Controls resource allocation and scaling:

```json
{
  "min_instances": 0,      // Scale to zero when idle
  "max_instances": 1,      // Maximum instances
  "resource_limits": {
    "cpu": "1",            // CPU cores per instance
    "memory": "1Gi"        // Memory per instance
  }
}
```

**Key parameters:**
- `min_instances`: Minimum running instances (0 = scale to zero)
- `max_instances`: Maximum instances for auto-scaling
- `cpu`: CPU cores (0.5, 1, 2, 4, etc.)
- `memory`: RAM (512Mi, 1Gi, 2Gi, 4Gi, etc.)

### 2. Environment Variables

**File: `.env`**

Controls cloud behavior:

**Development (Google AI Studio):**
```bash
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your-api-key
```

**Production (Vertex AI):**
```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_LOCATION="global"
# API key from Secret Manager
```

### 3. Memory Bank

**Session Memory vs Memory Bank:**

Session Memory:
- Scope: Single conversation
- Persistence: Lost when session ends
- Use case: "What did I say earlier?"
- Setup: Automatic

Memory Bank:
- Scope: All conversations
- Persistence: Permanent
- Use case: "What's my favorite city?"
- Setup: Requires memory_service

**When deployed to Agent Engine:**
- `InMemoryMemoryService` → Vertex AI Memory Bank
- LLM-powered consolidation
- Semantic search capabilities

### 4. Model Selection

Choose model based on requirements:

| Model | Cost | Speed | Use Case |
|-------|------|-------|----------|
| `gemini-2.5-flash-lite` | Lowest | Fastest | Simple Q&A, testing |
| `gemini-2.5-flash` | Low | Fast | Most production tasks |
| `gemini-2.5-pro` | Higher | Slower | Complex reasoning |

**Recommendations:**
- Development/Testing: `gemini-2.5-flash-lite`
- Production (general): `gemini-2.5-flash`
- Production (complex): `gemini-2.5-pro`

## 🛠️ Troubleshooting

### Deployment fails with "API not enabled"
```powershell
# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable logging.googleapis.com
```

### Authentication errors
```powershell
# Re-authenticate with gcloud
gcloud auth application-default login

# Verify authentication
gcloud auth list
```

### "Project not found" errors
```powershell
# Verify project ID
gcloud config get-value project

# Set correct project
gcloud config set project your-project-id
```

### Deployment takes too long
- Normal deployment time: 2-5 minutes
- If >10 minutes, check Cloud Console for errors
- Verify all APIs are enabled
- Check Cloud Build logs

### Cannot query deployed agent
```python
# Verify agent exists
from vertexai import agent_engines
agents_list = list(agent_engines.list())
print(agents_list)

# Check region matches deployment
vertexai.init(project="project-id", location="us-west1")
```

## 💰 Cost Management

### Free Tier
- Agent Engine offers monthly free tier
- Free tier details: [Agent Engine pricing](https://cloud.google.com/vertex-ai/pricing#agent-engine)
- New GCP accounts get $300 free credits (90 days)

### Cost Factors
1. **Running instances** - Based on min_instances and resource_limits
2. **API calls** - Gemini model calls (input/output tokens)
3. **Storage** - Logs, traces, Memory Bank
4. **Network** - Data transfer (usually minimal)

### Cost Optimization
1. **Scale to zero for dev/test:**
   ```json
   {"min_instances": 0, "max_instances": 1}
   ```

2. **Use efficient models:**
   - `gemini-2.5-flash-lite` (lowest cost)
   - Avoid `gemini-2.5-pro` unless needed

3. **Delete test deployments:**
   ```python
   agent_engines.delete(resource_name=agent.resource_name, force=True)
   ```

4. **Set budget alerts:**
   - Go to [Billing](https://console.cloud.google.com/billing)
   - Set up budget alerts at $10, $50, $100

### Cleanup Checklist
- ✅ Delete test agents after learning
- ✅ Verify deletion in Console
- ✅ Check for orphaned resources
- ✅ Monitor billing dashboard

## 📚 Additional Resources

### ADK Documentation
- [Deploy to Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-agent-engine)
- [Deploy to Cloud Run](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-cloud-run)
- [Deploy to GKE](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-gke)

### Memory Bank
- [ADK Memory Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/memory)
- [Memory Tools](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/memory-tools)
- [Vertex AI Memory Bank](https://cloud.google.com/vertex-ai/docs/memory-bank)

### Google Cloud
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-engine)
- [Free Trial](https://cloud.google.com/free)
- [Pricing](https://cloud.google.com/vertex-ai/pricing)

## ✅ Pre-Deployment Checklist

Before deploying to production:

- [ ] Tested agent locally (`adk run`)
- [ ] Configured `.agent_engine_config.json` for workload
- [ ] Set up `.env` with production settings
- [ ] Added `LoggingPlugin` for observability
- [ ] Configured API keys via Secret Manager (not hardcoded)
- [ ] Set up monitoring and alerts
- [ ] Tested with realistic traffic
- [ ] Implemented error handling
- [ ] Documented deployment process
- [ ] Set up budget alerts
- [ ] Have rollback plan ready

## 🎓 What's Next?

Congratulations! You've completed the 5-day AI Agents course! 🎉

**You now know how to:**
- ✅ Build agents with tools and instructions (Day 1)
- ✅ Create advanced tool patterns (Day 2)
- ✅ Manage sessions and memory (Day 3)
- ✅ Monitor and evaluate agents (Day 4)
- ✅ Deploy agents to production (Day 5)

**Next steps:**
- Build your own AI agents with ADK
- Share your projects on Kaggle Discord
- Explore advanced patterns in ADK documentation
- Deploy your agents to production!

---

**Questions?** Check the [main course README](../../README.md) or ask on the [Kaggle Discord](https://discord.gg/kaggle).
