"""
Standalone Script: Production Configuration Best Practices

This script demonstrates production-ready configuration for deployed agents.

KEY CONCEPTS:
- Resource limits: CPU, memory, instance scaling
- Environment variables: Cloud configuration
- Model selection: Cost vs capability tradeoffs
- Monitoring: Logging, tracing, error handling
- Security: API keys, authentication, secrets

PRODUCTION CONFIGURATION FILES:
1. .agent_engine_config.json - Resource allocation
2. .env - Environment variables
3. requirements.txt - Dependency management
4. agent.py - Production-ready code

WHAT THIS SCRIPT TEACHES:
- How to configure resources for different workloads
- When to use different deployment options
- Best practices for production agents
- Cost optimization strategies
- Monitoring and observability setup

CONFIGURATION SCENARIOS:
1. Development/Testing: Minimal resources, scales to zero
2. Production (Low Traffic): 1 instance, auto-scaling
3. Production (High Traffic): Multiple instances, reserved capacity
4. Cost-Optimized: Smallest viable configuration
5. Performance-Optimized: Maximum resources, low latency

USAGE:
    python Day5/5b-agent-deployment/03_production_config.py
    
    # This script is educational - it shows configuration patterns
    # Apply these patterns to your agent deployments
"""

import json


def print_configuration_guide():
    """Print comprehensive production configuration guide."""
    
    print("=" * 70)
    print("⚙️  Production Configuration Best Practices")
    print("=" * 70)
    
    # Configuration Files Overview
    print("\n📁 CONFIGURATION FILES")
    print("-" * 70)
    print("\nYour agent needs 4 configuration files for production:\n")
    print("1. .agent_engine_config.json - Resource limits and scaling")
    print("2. .env - Environment variables and cloud config")
    print("3. requirements.txt - Python dependencies")
    print("4. agent.py - Agent code with production patterns")
    
    # Agent Engine Config Scenarios
    print("\n" + "=" * 70)
    print("📊 SCENARIO 1: Development/Testing")
    print("=" * 70)
    print("\nUse Case: Testing, demos, learning")
    print("Cost: Minimal (scales to zero when idle)")
    print()
    
    dev_config = {
        "min_instances": 0,  # Scale to zero when idle
        "max_instances": 1,  # Only 1 instance max
        "resource_limits": {
            "cpu": "1",      # 1 CPU core
            "memory": "1Gi"  # 1 GB memory
        }
    }
    
    print("📄 .agent_engine_config.json:")
    print(json.dumps(dev_config, indent=2))
    print()
    print("✅ Pros:")
    print("   • Minimal cost (scales to zero)")
    print("   • Fast enough for testing")
    print("   • Good for demos and learning")
    print()
    print("⚠️  Cons:")
    print("   • Cold start latency (when scaling from zero)")
    print("   • Limited capacity (1 instance max)")
    print("   • Not suitable for production traffic")
    
    # Production Low Traffic
    print("\n" + "=" * 70)
    print("📊 SCENARIO 2: Production (Low Traffic)")
    print("=" * 70)
    print("\nUse Case: Small production app, <100 requests/hour")
    print("Cost: Low (1 instance always running)")
    print()
    
    prod_low_config = {
        "min_instances": 1,  # Always 1 instance running
        "max_instances": 3,  # Scale up to 3 if needed
        "resource_limits": {
            "cpu": "2",      # 2 CPU cores
            "memory": "2Gi"  # 2 GB memory
        }
    }
    
    print("📄 .agent_engine_config.json:")
    print(json.dumps(prod_low_config, indent=2))
    print()
    print("✅ Pros:")
    print("   • No cold start (1 instance always ready)")
    print("   • Auto-scales up to 3 instances if needed")
    print("   • Good for small production apps")
    print()
    print("⚠️  Considerations:")
    print("   • 1 instance always running (not free)")
    print("   • May not handle traffic spikes well")
    
    # Production High Traffic
    print("\n" + "=" * 70)
    print("📊 SCENARIO 3: Production (High Traffic)")
    print("=" * 70)
    print("\nUse Case: Large production app, >1000 requests/hour")
    print("Cost: Higher (multiple instances, reserved capacity)")
    print()
    
    prod_high_config = {
        "min_instances": 3,   # Always 3 instances running
        "max_instances": 10,  # Scale up to 10 if needed
        "resource_limits": {
            "cpu": "4",       # 4 CPU cores
            "memory": "4Gi"   # 4 GB memory
        }
    }
    
    print("📄 .agent_engine_config.json:")
    print(json.dumps(prod_high_config, indent=2))
    print()
    print("✅ Pros:")
    print("   • Always ready (3 instances minimum)")
    print("   • Handles traffic spikes (up to 10 instances)")
    print("   • Low latency (more resources)")
    print()
    print("⚠️  Considerations:")
    print("   • Higher cost (3 instances always running)")
    print("   • May be overkill for smaller apps")
    
    # Cost-Optimized
    print("\n" + "=" * 70)
    print("📊 SCENARIO 4: Cost-Optimized")
    print("=" * 70)
    print("\nUse Case: Budget-constrained, latency not critical")
    print("Cost: Minimal (smallest viable configuration)")
    print()
    
    cost_config = {
        "min_instances": 0,     # Scale to zero
        "max_instances": 1,     # Only 1 instance max
        "resource_limits": {
            "cpu": "0.5",       # Half CPU core
            "memory": "512Mi"   # 512 MB memory
        }
    }
    
    print("📄 .agent_engine_config.json:")
    print(json.dumps(cost_config, indent=2))
    print()
    print("✅ Pros:")
    print("   • Absolute minimal cost")
    print("   • Scales to zero when idle")
    print("   • Good for hobby projects")
    print()
    print("⚠️  Cons:")
    print("   • Cold start latency")
    print("   • Limited resources (may be slow)")
    print("   • Not for production use")
    
    # Environment Configuration
    print("\n" + "=" * 70)
    print("🌍 ENVIRONMENT CONFIGURATION (.env)")
    print("=" * 70)
    print("\nEnvironment variables control cloud behavior:\n")
    
    print("📄 Development .env:")
    print("-" * 70)
    print("""
# Use Google AI Studio (free tier)
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your-api-key
    """.strip())
    
    print("\n\n📄 Production .env:")
    print("-" * 70)
    print("""
# Use Vertex AI (production)
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_LOCATION="global"
# API key from Secret Manager, not hardcoded
    """.strip())
    
    print("\n\n⚠️  SECURITY BEST PRACTICES:")
    print("-" * 70)
    print("❌ NEVER commit .env files to git!")
    print("❌ NEVER hardcode API keys in code!")
    print("✅ Use Google Cloud Secret Manager for production")
    print("✅ Use service accounts with minimal permissions")
    print("✅ Rotate API keys regularly")
    
    # Model Selection
    print("\n" + "=" * 70)
    print("🤖 MODEL SELECTION GUIDE")
    print("=" * 70)
    print("\nChoose model based on use case:\n")
    
    print("┌────────────────────────┬──────────────┬────────────┬─────────────┐")
    print("│ Model                  │ Cost         │ Speed      │ Use Case    │")
    print("├────────────────────────┼──────────────┼────────────┼─────────────┤")
    print("│ gemini-2.5-flash-lite  │ Lowest       │ Fastest    │ Simple Q&A  │")
    print("│ gemini-2.5-flash       │ Low          │ Fast       │ Most tasks  │")
    print("│ gemini-2.5-pro         │ Higher       │ Slower     │ Complex     │")
    print("└────────────────────────┴──────────────┴────────────┴─────────────┘")
    
    print("\n💡 Recommendations:")
    print("   • Development/Testing: gemini-2.5-flash-lite")
    print("   • Production (general): gemini-2.5-flash")
    print("   • Production (complex): gemini-2.5-pro")
    
    # Monitoring
    print("\n" + "=" * 70)
    print("📈 MONITORING & OBSERVABILITY")
    print("=" * 70)
    print("\nProduction agents need comprehensive monitoring:\n")
    
    print("1. Logging:")
    print("   • Use LoggingPlugin for automatic event capture")
    print("   • View logs in Cloud Logging Console")
    print("   • Set up log-based alerts")
    print()
    print("2. Metrics:")
    print("   • Track request count, latency, errors")
    print("   • Monitor in Cloud Monitoring")
    print("   • Set up metric-based alerts")
    print()
    print("3. Tracing:")
    print("   • Enable enable_tracing=True in agent config")
    print("   • View traces in Cloud Trace")
    print("   • Debug performance issues")
    print()
    print("4. Error Tracking:")
    print("   • Set up error reporting")
    print("   • Configure PagerDuty/OpsGenie integration")
    print("   • Implement retry logic")
    
    print("\nExample agent.py with monitoring:")
    print("-" * 70)
    print("""
from google.adk.agents import Agent
from google.adk.plugins.logging_plugin import LoggingPlugin

root_agent = Agent(
    name="production_agent",
    model="gemini-2.5-flash",
    tools=[...],
    enable_tracing=True,  # Enable Cloud Trace
)

# Add logging plugin for comprehensive logs
runner = Runner(
    agent=root_agent,
    plugins=[LoggingPlugin()]
)
    """.strip())
    
    # Deployment Comparison
    print("\n" + "=" * 70)
    print("🔷 DEPLOYMENT OPTIONS COMPARISON")
    print("=" * 70)
    print()
    print("┌──────────────┬────────────────┬─────────────┬────────────────┐")
    print("│ Platform     │ Best For       │ Complexity  │ Cost           │")
    print("├──────────────┼────────────────┼─────────────┼────────────────┤")
    print("│ Agent Engine │ AI agents      │ Low         │ Pay per use    │")
    print("│ Cloud Run    │ Demos, APIs    │ Very low    │ Very low       │")
    print("│ GKE          │ Enterprise     │ High        │ Higher         │")
    print("└──────────────┴────────────────┴─────────────┴────────────────┘")
    
    print("\n💡 Decision Tree:")
    print("   • Learning/demos? → Cloud Run")
    print("   • Production AI agent? → Agent Engine")
    print("   • Complex microservices? → GKE")
    
    # Cost Optimization
    print("\n" + "=" * 70)
    print("💰 COST OPTIMIZATION STRATEGIES")
    print("=" * 70)
    print("\n1. Resource Configuration:")
    print("   • Set min_instances: 0 for dev/testing")
    print("   • Use smallest viable CPU/memory")
    print("   • Monitor and adjust based on metrics")
    print()
    print("2. Model Selection:")
    print("   • Use flash-lite for simple tasks")
    print("   • Reserve pro models for complex tasks")
    print("   • Implement caching where possible")
    print()
    print("3. Scaling:")
    print("   • Scale to zero when idle (dev/test)")
    print("   • Use auto-scaling for variable traffic")
    print("   • Set max_instances to prevent runaway costs")
    print()
    print("4. Monitoring:")
    print("   • Set up budget alerts in GCP")
    print("   • Track cost per request")
    print("   • Identify expensive operations")
    print()
    print("5. Cleanup:")
    print("   • DELETE test deployments immediately")
    print("   • Remove unused resources")
    print("   • Use lifecycle policies for storage")
    
    # Checklist
    print("\n" + "=" * 70)
    print("✅ PRE-DEPLOYMENT CHECKLIST")
    print("=" * 70)
    print("\nBefore deploying to production:\n")
    print("□ Tested agent locally (adk run)")
    print("□ Configured .agent_engine_config.json for workload")
    print("□ Set up .env with production settings")
    print("□ Added LoggingPlugin for observability")
    print("□ Enabled tracing (enable_tracing=True)")
    print("□ Configured API keys via Secret Manager")
    print("□ Set up monitoring and alerts")
    print("□ Tested with realistic traffic")
    print("□ Implemented error handling and retries")
    print("□ Documented deployment process")
    print("□ Set up budget alerts")
    print("□ Have rollback plan ready")
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 KEY TAKEAWAYS")
    print("=" * 70)
    print("\n1. Configuration matters:")
    print("   • Choose resources based on workload")
    print("   • Scale to zero for dev/test to save costs")
    print()
    print("2. Security is critical:")
    print("   • Never commit secrets to git")
    print("   • Use Secret Manager for production")
    print()
    print("3. Monitor everything:")
    print("   • Logs, metrics, traces are essential")
    print("   • Set up alerts before issues occur")
    print()
    print("4. Optimize costs:")
    print("   • Use smallest viable resources")
    print("   • Delete test deployments immediately")
    print("   • Monitor spending regularly")
    print()
    print("5. Plan for scale:")
    print("   • Test with realistic traffic")
    print("   • Use auto-scaling for variable loads")
    print("   • Have rollback plan ready")
    
    print("\n" + "=" * 70)
    print("✅ Configuration Guide Complete!")
    print("=" * 70)
    print("\n💡 Apply these patterns to your production deployments.")
    print("   Start conservative, monitor, and adjust as needed.")


if __name__ == "__main__":
    print_configuration_guide()
