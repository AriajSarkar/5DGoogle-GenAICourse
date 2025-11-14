"""
Standalone Script: Deploy ADK Agent to Vertex AI Agent Engine

This script demonstrates the complete workflow for deploying an ADK agent to production.

KEY CONCEPTS:
- adk deploy agent_engine: CLI command to deploy agents
- Agent Engine configuration: Resource limits, scaling, environment
- Deployment files: agent.py, requirements.txt, .env, .agent_engine_config.json
- Testing deployed agents: Connecting and querying via SDK

WHAT THIS SCRIPT DOES:
1. Shows how to prepare deployment files
2. Demonstrates adk deploy command usage
3. Explains how to test deployed agents
4. Shows how to manage (list, query, delete) deployed agents

⚠️ IMPORTANT: Prerequisites
This script requires:
1. Google Cloud account with billing enabled
2. Vertex AI API enabled in your project
3. gcloud CLI authenticated
4. Project ID configured

DEPLOYMENT WORKFLOW:
1. Create agent folder with proper structure:
   weather_agent/
   ├── __init__.py
   ├── agent.py                     # Agent definition (root_agent variable)
   ├── requirements.txt              # Dependencies
   ├── .env                          # Environment config
   └── .agent_engine_config.json    # Resource limits

2. Deploy using ADK CLI:
   adk deploy agent_engine weather_agent/ \\
       --project=your-project-id \\
       --region=us-west1

3. Test deployed agent:
   - Get agent via SDK
   - Send queries
   - Monitor responses

4. Cleanup:
   - Delete agent to avoid costs
   - Verify deletion in console

USAGE:
    # Set your project ID
    $env:GOOGLE_CLOUD_PROJECT="your-project-id"
    
    # Run this script for guidance
    python Day5/5b-agent-deployment/01_deploy_to_agent_engine.py
    
    # Or deploy directly (requires GCP setup)
    adk deploy agent_engine Day5/5b-agent-deployment/weather_agent_deploy/ `
        --project=$env:GOOGLE_CLOUD_PROJECT `
        --region=us-west1

COST MANAGEMENT:
- Agent Engine offers monthly free tier
- Agent deployed in this example should stay within free tier if cleaned up promptly
- Always delete test deployments to avoid ongoing costs

See Day 5b README for complete deployment guide.
"""

import os


def print_deployment_guide():
    """Print comprehensive deployment guide."""
    
    print("=" * 70)
    print("🚀 ADK Agent Deployment Guide: Vertex AI Agent Engine")
    print("=" * 70)
    
    # Prerequisites
    print("\n📋 PREREQUISITES")
    print("-" * 70)
    print("✅ Google Cloud account with billing enabled")
    print("✅ Project created in Google Cloud Console")
    print("✅ Vertex AI API enabled")
    print("✅ gcloud CLI installed and authenticated")
    print("✅ ADK installed with: pip install google-adk")
    print()
    print("Setup Steps:")
    print("1. Create GCP account: https://console.cloud.google.com")
    print("2. Create project and note PROJECT_ID")
    print("3. Enable APIs:")
    print("   - Vertex AI API")
    print("   - Cloud Storage API")
    print("   - Cloud Logging API")
    print("4. Install gcloud CLI: https://cloud.google.com/sdk/install")
    print("5. Authenticate: gcloud auth application-default login")
    
    # File Structure
    print("\n" + "=" * 70)
    print("📁 STEP 1: Prepare Deployment Files")
    print("=" * 70)
    print("\nYour agent folder must have this structure:")
    print()
    print("weather_agent/")
    print("├── __init__.py                  # Exports root_agent")
    print("├── agent.py                     # Agent definition")
    print("├── requirements.txt             # Dependencies")
    print("├── .env                         # Environment config")
    print("└── .agent_engine_config.json   # Resource limits")
    print()
    
    # File Contents
    print("📄 File: agent.py")
    print("-" * 70)
    print("""
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    # Your tool implementation
    ...

root_agent = Agent(
    name="weather_assistant",
    model="gemini-2.5-flash-lite",
    tools=[get_weather],
    ...
)
    """.strip())
    
    print("\n📄 File: __init__.py")
    print("-" * 70)
    print("""
from .agent import root_agent
__all__ = ["root_agent"]
    """.strip())
    
    print("\n📄 File: requirements.txt")
    print("-" * 70)
    print("google-adk")
    
    print("\n📄 File: .env")
    print("-" * 70)
    print("""
GOOGLE_CLOUD_LOCATION="global"
GOOGLE_GENAI_USE_VERTEXAI=1
    """.strip())
    
    print("\n📄 File: .agent_engine_config.json")
    print("-" * 70)
    print("""{
  "min_instances": 0,
  "max_instances": 1,
  "resource_limits": {"cpu": "1", "memory": "1Gi"}
}""")
    
    # Deploy Command
    print("\n" + "=" * 70)
    print("🚢 STEP 2: Deploy Agent")
    print("=" * 70)
    print("\nPowerShell:")
    print("-" * 70)
    print("""
# Set your project ID
$env:GOOGLE_CLOUD_PROJECT="your-project-id"

# Deploy to Agent Engine
adk deploy agent_engine Day5/5b-agent-deployment/weather_agent_deploy/ `
    --project=$env:GOOGLE_CLOUD_PROJECT `
    --region=us-west1
    """.strip())
    
    print("\n\nWhat happens during deployment:")
    print("1. ADK packages your agent code")
    print("2. Uploads to Agent Engine")
    print("3. Creates containerized deployment")
    print("4. Returns resource name: projects/.../reasoningEngines/...")
    print()
    print("⏱️  Deployment takes 2-5 minutes")
    
    # Test Deployed Agent
    print("\n" + "=" * 70)
    print("🧪 STEP 3: Test Deployed Agent")
    print("=" * 70)
    print("\nPython code to query deployed agent:")
    print("-" * 70)
    print("""
import vertexai
from vertexai import agent_engines

# Initialize
vertexai.init(project="your-project-id", location="us-west1")

# Get deployed agent
agents_list = list(agent_engines.list())
remote_agent = agents_list[0]  # Most recent

# Query agent
async for item in remote_agent.async_stream_query(
    message="What's the weather in Tokyo?",
    user_id="user_123"
):
    print(item)
    """.strip())
    
    # Cleanup
    print("\n" + "=" * 70)
    print("🧹 STEP 4: Cleanup (IMPORTANT!)")
    print("=" * 70)
    print("\n⚠️  ALWAYS DELETE TEST DEPLOYMENTS TO AVOID COSTS")
    print()
    print("Python code to delete agent:")
    print("-" * 70)
    print("""
from vertexai import agent_engines

# Delete agent
agent_engines.delete(resource_name=remote_agent.resource_name, force=True)

print("✅ Agent deleted successfully")
    """.strip())
    
    print("\n\nOr use gcloud CLI:")
    print("-" * 70)
    print("""
# List agents
gcloud ai agents list --region=us-west1

# Delete specific agent
gcloud ai agents delete AGENT_ID --region=us-west1
    """.strip())
    
    # Cost Management
    print("\n" + "=" * 70)
    print("💰 COST MANAGEMENT")
    print("=" * 70)
    print("\n✅ Free Tier:")
    print("   - Agent Engine offers monthly free tier")
    print("   - This demo should stay within free tier if cleaned up promptly")
    print()
    print("⚠️  Cost Factors:")
    print("   - Running instances (configured in .agent_engine_config.json)")
    print("   - API calls to Gemini models")
    print("   - Storage for logs and traces")
    print()
    print("💡 Best Practices:")
    print("   - Set min_instances: 0 (scales to zero when idle)")
    print("   - Delete test deployments immediately after testing")
    print("   - Use gemini-2.5-flash-lite for cost efficiency")
    print("   - Monitor usage in GCP Console")
    
    # Other Deployment Options
    print("\n" + "=" * 70)
    print("🔷 OTHER DEPLOYMENT OPTIONS")
    print("=" * 70)
    print("\n1. Cloud Run (Serverless):")
    print("   adk deploy cloud_run weather_agent/")
    print("   - Easiest to start")
    print("   - Perfect for demos")
    print()
    print("2. GKE (Kubernetes):")
    print("   adk deploy gke weather_agent/")
    print("   - Full control")
    print("   - Complex multi-agent systems")
    print()
    print("3. Local Testing:")
    print("   adk run weather_agent/")
    print("   - Free, no cloud costs")
    print("   - Great for development")
    
    # Next Steps
    print("\n" + "=" * 70)
    print("🎯 NEXT STEPS")
    print("=" * 70)
    print("\n1. ✅ Review the weather_agent_deploy/ folder structure")
    print("2. ✅ Set up your GCP project and enable APIs")
    print("3. ✅ Deploy the weather agent to Agent Engine")
    print("4. ✅ Test with sample queries")
    print("5. ✅ DELETE the deployment to avoid costs")
    print("6. ✅ Try deploying with Memory Bank (memory_enabled_agent/)")
    
    # Resources
    print("\n" + "=" * 70)
    print("📚 RESOURCES")
    print("=" * 70)
    print("\n• ADK Deployment Guide:")
    print("  https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/deploy-agent-engine")
    print("\n• Agent Engine Documentation:")
    print("  https://cloud.google.com/vertex-ai/docs/agent-engine")
    print("\n• GCP Free Trial:")
    print("  https://cloud.google.com/free")
    print("\n• Pricing Information:")
    print("  https://cloud.google.com/vertex-ai/pricing")
    
    print("\n" + "=" * 70)
    print("✅ Deployment Guide Complete!")
    print("=" * 70)
    print("\n💡 This script is a GUIDE for understanding deployment.")
    print("   To actually deploy, follow the steps above with your GCP project.")
    print("\n⚠️  Remember: Always delete test deployments to avoid costs!")


if __name__ == "__main__":
    print_deployment_guide()
