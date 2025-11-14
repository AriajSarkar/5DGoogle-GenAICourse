"""
Standalone Script: Full A2A Ecosystem Demo

This script demonstrates a complete A2A architecture with multiple considerations.

KEY CONCEPTS:
- A2A vs Local Sub-Agents: Decision tree for when to use each
- Multiple Remote Agents: Coordinating across external services
- Hybrid Architecture: Combining A2A agents with local tools
- Real-World Patterns: Microservices, cross-organization integration

WHAT THIS SCRIPT DOES:
1. Creates a coordinator agent that integrates:
   - Remote A2A Agent: Product Catalog (external vendor)
   - Local Tool: Tax calculation (internal logic)
2. Demonstrates when to use A2A vs local tools
3. Shows complete e-commerce workflow with A2A integration

ARCHITECTURE:
E-Commerce Coordinator Agent
    ├── RemoteA2aAgent: Product Catalog (http://localhost:8001)
    │   └── Why A2A: External vendor, different organization
    └── Local Tool: calculate_tax()
        └── Why Local: Simple calc, internal logic, fast execution

DECISION TREE: A2A vs Local
┌─────────────────────────────────────────────────────────┐
│ Use A2A When:                                           │
│ ✅ Agent owned by different team/organization          │
│ ✅ Agent runs on different infrastructure              │
│ ✅ Formal API contract needed                          │
│ ✅ Cross-language/framework integration required       │
│ ✅ Network latency acceptable                          │
│                                                         │
│ Use Local Sub-Agents When:                             │
│ ✅ Same codebase, internal to your team                │
│ ✅ Same process/machine                                │
│ ✅ Need low latency                                    │
│ ✅ No formal contract needed                           │
│ ✅ Internal interface                                  │
└─────────────────────────────────────────────────────────┘

PREREQUISITES:
Start Product Catalog Server:
    python Day5/5a-agent2agent-communication/01_a2a_server.py

USAGE:
    python Day5/5a-agent2agent-communication/03_a2a_hybrid.py
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


def calculate_tax(state: str, price: float) -> dict:
    """
    Calculate sales tax based on state.
    
    This is a LOCAL tool - kept in the same agent because:
    - Simple calculation (no external dependency)
    - Fast execution (no network latency)
    - Internal business logic (your organization owns it)
    - No cross-organization coordination needed
    
    Args:
        state: US state code (e.g., "CA", "NY", "TX")
        price: Product price in dollars
    
    Returns:
        dict: Tax amount and total price with tax
    """
    tax_rates = {
        "CA": 0.0725,  # California: 7.25%
        "NY": 0.0400,  # New York: 4%
        "TX": 0.0625,  # Texas: 6.25%
        "FL": 0.0600,  # Florida: 6%
        "WA": 0.0650,  # Washington: 6.5%
    }
    
    state_upper = state.upper()
    tax_rate = tax_rates.get(state_upper, 0.0700)  # Default: 7%
    
    tax_amount = price * tax_rate
    total = price + tax_amount
    
    return {
        "status": "success",
        "state": state_upper,
        "tax_rate": f"{tax_rate * 100:.2f}%",
        "tax_amount": f"${tax_amount:.2f}",
        "total": f"${total:.2f}",
        "breakdown": f"Product: ${price:.2f} + Tax ({tax_rate*100:.2f}%): ${tax_amount:.2f} = Total: ${total:.2f}"
    }


async def test_ecommerce_workflow(user_query: str, coordinator_agent: LlmAgent):
    """Test e-commerce workflow with A2A + local tools."""
    session_service = InMemorySessionService()
    
    app_name = "ecommerce_app"
    user_id = "demo_user"
    session_id = f"demo_session_{uuid.uuid4().hex[:8]}"
    
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    runner = Runner(
        agent=coordinator_agent,
        app_name=app_name,
        session_service=session_service
    )
    
    test_content = types.Content(parts=[types.Part(text=user_query)])
    
    print(f"\n👤 Customer: {user_query}")
    print(f"\n🛒 E-Commerce Coordinator response:")
    print("-" * 60)
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=test_content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(part.text)
    
    print("-" * 60)


async def main():
    """
    Main function demonstrating hybrid A2A + local tool architecture.
    
    FLOW:
    1. Create RemoteA2aAgent for Product Catalog (A2A)
    2. Create local calculate_tax tool (Local)
    3. Create E-Commerce Coordinator that uses both
    4. Test complete workflows
    """
    print("=" * 60)
    print("🛒 A2A Hybrid Architecture Demo: E-Commerce System")
    print("=" * 60)
    
    # Architecture Overview
    print("\n📐 Architecture Overview:")
    print("-" * 60)
    print("E-Commerce Coordinator Agent")
    print("    ├── RemoteA2aAgent: Product Catalog (A2A)")
    print("    │   ├── URL: http://localhost:8001")
    print("    │   ├── Why A2A: External vendor, different org")
    print("    │   └── Provides: Product info, pricing, availability")
    print("    └── Local Tool: calculate_tax()")
    print("        ├── Why Local: Simple calc, internal logic")
    print("        └── Provides: Sales tax calculation")
    print("-" * 60)
    
    # Step 1: Create Remote A2A Agent
    print("\n🌐 Step 1: Creating RemoteA2aAgent (Product Catalog)...")
    try:
        remote_product_catalog = RemoteA2aAgent(
            name="product_catalog_agent",
            description="External vendor's product catalog with pricing and availability.",
            agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
        )
        print("   ✅ Connected to Product Catalog Agent (A2A)")
    except Exception as e:
        print(f"\n❌ Error: Could not connect to Product Catalog Server!")
        print(f"   Details: {e}")
        print(f"\n💡 Start the server first:")
        print("   python Day5/5a-agent2agent-communication/01_a2a_server.py")
        return
    
    # Step 2: Create E-Commerce Coordinator
    print("\n🛒 Step 2: Creating E-Commerce Coordinator...")
    coordinator_agent = LlmAgent(
        model=Gemini(model=get_text_model()),
        name="ecommerce_coordinator",
        description="E-commerce coordinator integrating external services and internal logic.",
        instruction="""
        You are an e-commerce coordinator that helps customers with purchases.
        
        YOUR CAPABILITIES:
        1. Product Information: Use product_catalog_agent (A2A remote) to get pricing and availability
        2. Tax Calculation: Use calculate_tax (local tool) to compute sales tax
        
        WORKFLOW:
        When customers ask about purchasing products:
        1. Get product details from product_catalog_agent
        2. If customer mentions a state, calculate tax using calculate_tax tool
        3. Provide clear summary with:
           - Product details (name, price, availability)
           - Tax amount (if applicable)
           - Total cost (if applicable)
        
        IMPORTANT DECISION MAKING:
        - Use A2A agents for: External data (products, inventory, shipping)
        - Use local tools for: Internal calculations (tax, discounts, promotions)
        
        Be professional and helpful. Always verify product availability before confirming orders.
        
        Example Response Format:
        "The iPhone 15 Pro costs $999 and we have 8 units in stock. 
         With California tax (7.25%), your total would be $1,071.42."
        """,
        sub_agents=[remote_product_catalog],  # A2A remote agent
        tools=[calculate_tax]  # Local tool
    )
    print("   ✅ Coordinator created with hybrid architecture")
    print("   📌 Sub-agents: 1 (RemoteA2aAgent)")
    print("   🔧 Tools: 1 (calculate_tax)")
    
    # Step 3: Test workflows
    print("\n" + "=" * 60)
    print("🧪 Step 3: Testing E-Commerce Workflows")
    print("=" * 60)
    
    # Test 1: Product inquiry only (A2A)
    print("\n📝 Test 1: Product inquiry (A2A only)")
    await test_ecommerce_workflow(
        "What's the price of the iPhone 15 Pro?",
        coordinator_agent
    )
    
    # Test 2: Product + Tax (A2A + Local)
    print("\n\n📝 Test 2: Product inquiry with tax calculation (A2A + Local)")
    await test_ecommerce_workflow(
        "I want to buy an iPhone 15 Pro in California. What's the total cost with tax?",
        coordinator_agent
    )
    
    # Test 3: Multiple products comparison (A2A)
    print("\n\n📝 Test 3: Product comparison (A2A)")
    await test_ecommerce_workflow(
        "Compare the Dell XPS 15 and Samsung Galaxy S24 for me.",
        coordinator_agent
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ A2A Hybrid Architecture Demo Complete!")
    print("=" * 60)
    
    print("\n📊 Architecture Decisions Explained:")
    print("-" * 60)
    print("✅ Product Catalog → A2A Remote Agent")
    print("   Reasons:")
    print("   • Owned by external vendor (different organization)")
    print("   • Vendor controls data and infrastructure")
    print("   • Formal API contract needed")
    print("   • Vendor may use different language/framework")
    print("   • Network latency acceptable for product lookups")
    print()
    print("✅ Tax Calculation → Local Tool")
    print("   Reasons:")
    print("   • Simple calculation (no external dependency)")
    print("   • Your organization owns tax logic")
    print("   • Fast execution (no network call)")
    print("   • Internal business rule")
    print("   • No cross-organization coordination needed")
    print("-" * 60)
    
    print("\n💡 Real-World Applications:")
    print("   🏢 Microservices: Each external service as A2A agent")
    print("   🤝 Third-party Integration: Consume vendor agents")
    print("   🌍 Cross-language: Java service, Python agent")
    print("   🏛️ Cross-organization: Partner services via A2A")
    print("   ⚡ Performance: Keep fast operations local")
    
    print("\n📚 When to Choose A2A vs Local:")
    print("   A2A: External, cross-org, formal contract, network OK")
    print("   Local: Internal, same codebase, fast execution needed")


if __name__ == "__main__":
    asyncio.run(main())
