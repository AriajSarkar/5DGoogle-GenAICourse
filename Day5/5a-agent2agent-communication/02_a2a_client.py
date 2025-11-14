"""
Standalone Script: Consuming a Remote Agent via A2A Protocol

This script demonstrates how to consume a remote A2A agent using RemoteA2aAgent.

KEY CONCEPTS:
- RemoteA2aAgent: Client-side proxy that connects to A2A server
- Agent Card Discovery: Reads capabilities from /.well-known/agent-card.json
- Sub-Agent Pattern: Use remote agent like a local sub-agent
- Transparent Communication: ADK handles all A2A protocol details

WHAT THIS SCRIPT DOES:
1. Creates a RemoteA2aAgent pointing to Product Catalog Server
2. Creates a Customer Support Agent that uses the remote agent
3. Sends queries that trigger A2A communication
4. Displays responses with A2A interaction logs

PREREQUISITES:
1. Start the A2A server first:
   python Day5/5a-agent2agent-communication/01_a2a_server.py

2. Verify server is running:
   curl http://localhost:8001/.well-known/agent-card.json

USAGE:
    python Day5/5a-agent2agent-communication/02_a2a_client.py

WHAT HAPPENS BEHIND THE SCENES:
1. Customer asks Support Agent a question
2. Support Agent decides it needs product info
3. Support Agent calls remote_product_catalog_agent (RemoteA2aAgent)
4. RemoteA2aAgent sends HTTP POST to http://localhost:8001/tasks
5. Product Catalog Agent processes request and responds
6. RemoteA2aAgent receives response and passes to Support Agent
7. Support Agent formulates final answer
8. Customer gets complete response

All of this is TRANSPARENT - Support Agent doesn't know it's remote!
"""

import asyncio
import uuid
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from utils.model_config import get_text_model


# Load environment variables
load_dotenv()


async def test_a2a_communication(user_query: str, support_agent: LlmAgent):
    """
    Test A2A communication between Customer Support Agent and Product Catalog Agent.
    
    Args:
        user_query: Question to ask the Customer Support Agent
        support_agent: The customer support agent instance
    """
    # Setup session management
    session_service = InMemorySessionService()
    
    # Session identifiers
    app_name = "support_app"
    user_id = "demo_user"
    session_id = f"demo_session_{uuid.uuid4().hex[:8]}"
    
    # Create session
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Create runner
    runner = Runner(
        agent=support_agent,
        app_name=app_name,
        session_service=session_service
    )
    
    # Create user message
    test_content = types.Content(parts=[types.Part(text=user_query)])
    
    # Display query
    print(f"\n👤 Customer: {user_query}")
    print(f"\n🎧 Support Agent response:")
    print("-" * 60)
    
    # Run agent and stream response
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=test_content
    ):
        # Print final response only
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(part.text)
    
    print("-" * 60)


async def main():
    """
    Main function to demonstrate A2A client usage.
    
    FLOW:
    1. Create RemoteA2aAgent (client-side proxy)
    2. Create Customer Support Agent with remote sub-agent
    3. Test A2A communication with sample queries
    """
    print("=" * 60)
    print("🎧 A2A Client Demo: Customer Support Agent")
    print("=" * 60)
    
    # Step 1: Create RemoteA2aAgent
    print("\n🌐 Step 1: Creating RemoteA2aAgent...")
    print("   Connecting to: http://localhost:8001")
    print(f"   Agent card: http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}")
    
    try:
        remote_product_catalog_agent = RemoteA2aAgent(
            name="product_catalog_agent",
            description="Remote product catalog agent from external vendor.",
            agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
        )
        print("   ✅ RemoteA2aAgent created successfully!")
    except Exception as e:
        print(f"\n❌ Error: Could not connect to A2A server!")
        print(f"   Details: {e}")
        print(f"\n💡 Make sure the A2A server is running:")
        print("   python Day5/5a-agent2agent-communication/01_a2a_server.py")
        return
    
    # Step 2: Create Customer Support Agent
    print("\n🎧 Step 2: Creating Customer Support Agent...")
    customer_support_agent = LlmAgent(
        model=Gemini(model=get_text_model()),
        name="customer_support_agent",
        description="Customer support assistant that helps with product inquiries.",
        instruction="""
        You are a friendly and professional customer support agent.
        
        When customers ask about products:
        1. Use the product_catalog_agent sub-agent to look up product information
        2. Provide clear answers about pricing, availability, and specifications
        3. If a product is out of stock, mention expected availability
        4. Be helpful and professional
        
        IMPORTANT: Always get product information from the product_catalog_agent.
        Do not make up product details - always use the catalog agent.
        """,
        sub_agents=[remote_product_catalog_agent]  # Connect to remote A2A agent!
    )
    print("   ✅ Customer Support Agent created")
    print("   📌 Sub-agents: 1 (remote Product Catalog Agent via A2A)")
    
    # Step 3: Test A2A communication
    print("\n" + "=" * 60)
    print("🧪 Step 3: Testing A2A Communication")
    print("=" * 60)
    
    # Test 1: Simple product query
    print("\n📝 Test 1: Simple product query")
    await test_a2a_communication(
        "Can you tell me about the iPhone 15 Pro? Is it in stock?",
        customer_support_agent
    )
    
    # Test 2: Comparing multiple products
    print("\n\n📝 Test 2: Comparing multiple products")
    await test_a2a_communication(
        "I'm looking for a laptop. Can you compare the Dell XPS 15 and MacBook Pro 14?",
        customer_support_agent
    )
    
    # Test 3: Specific product inquiry
    print("\n\n📝 Test 3: Specific product inquiry")
    await test_a2a_communication(
        "What's the price of the Samsung Galaxy S24?",
        customer_support_agent
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ A2A Communication Tests Complete!")
    print("=" * 60)
    print("\n📊 What Just Happened:")
    print("   1. Customer Support Agent received your questions")
    print("   2. Agent decided it needed product information")
    print("   3. Agent called remote_product_catalog_agent (RemoteA2aAgent)")
    print("   4. RemoteA2aAgent sent HTTP POST to http://localhost:8001/tasks")
    print("   5. Product Catalog Agent processed request and responded")
    print("   6. RemoteA2aAgent received response and passed to Support Agent")
    print("   7. Support Agent formulated final answer")
    print("   8. You received the complete response")
    print("\n✨ Key Benefits:")
    print("   ✅ Transparent: Support Agent doesn't know catalog is remote")
    print("   ✅ Standard Protocol: Uses A2A - any compatible agent works")
    print("   ✅ Easy Integration: Just one line: sub_agents=[remote_agent]")
    print("   ✅ Separation: Catalog data lives in vendor's agent")
    print("\n💡 Real-World Applications:")
    print("   - Microservices: Each agent is independent service")
    print("   - Third-party Integration: Consume vendor agents")
    print("   - Cross-language: Catalog could be Java, Support Python")
    print("   - Cross-organization: Vendor hosts catalog, you integrate via A2A")


if __name__ == "__main__":
    asyncio.run(main())
