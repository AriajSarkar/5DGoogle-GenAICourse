"""
Full A2A Demo: Multi-Service Integration

This agent demonstrates a complete A2A ecosystem with multiple remote services.

KEY CONCEPTS:
- Multiple RemoteA2aAgent integrations (Product Catalog, Inventory, Shipping)
- Cross-organization agent collaboration
- Real-world microservices architecture
- A2A vs local sub-agents decision making

ARCHITECTURE:
Coordinator Agent (this agent)
    ├── RemoteA2aAgent: Product Catalog (external vendor)
    ├── RemoteA2aAgent: Inventory System (external service)
    └── RemoteA2aAgent: Shipping Service (external provider)

WHY A2A:
- Each service is owned by different organizations
- Services run on different infrastructure
- Formal API contracts needed
- Cross-language/framework support

PREREQUISITES:
Start all A2A servers first:
1. Product Catalog Server: python Day5/5a-agent2agent-communication/01_a2a_server.py
2. (Optional) Start additional mock servers for Inventory and Shipping

RUN WITH:
    adk run Day5/5a-agent2agent-communication/full_a2a_demo/
    
    # Then ask: "I want to buy an iPhone 15 Pro and ship it to California"
    # The agent will coordinate across multiple A2A services!
"""

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.models.google_llm import Gemini
from utils.model_config import get_text_model


# Remote A2A Agent 1: Product Catalog (external vendor)
remote_product_catalog = RemoteA2aAgent(
    name="product_catalog_agent",
    description="External vendor's product catalog with pricing and availability.",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)

# Remote A2A Agent 2: Inventory System (external service)
# NOTE: This would connect to a real inventory service in production
# For this demo, we'll note it but won't implement a second server
# remote_inventory_system = RemoteA2aAgent(
#     name="inventory_agent",
#     description="External inventory management system for stock tracking.",
#     agent_card=f"http://localhost:8002{AGENT_CARD_WELL_KNOWN_PATH}",
# )

# Remote A2A Agent 3: Shipping Service (external provider)
# NOTE: This would connect to a real shipping provider in production
# remote_shipping_service = RemoteA2aAgent(
#     name="shipping_agent",
#     description="External shipping provider for delivery estimates and tracking.",
#     agent_card=f"http://localhost:8003{AGENT_CARD_WELL_KNOWN_PATH}",
# )


# Local helper tool (demonstrates A2A vs local decision)
def calculate_tax(state: str, price: float) -> dict:
    """
    Calculate sales tax based on state.
    
    This is a LOCAL tool - kept in the same agent because:
    - Simple calculation (no external dependency)
    - Fast execution (no network latency)
    - Internal business logic (your organization owns it)
    
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
        "total": f"${total:.2f}"
    }


# Create the E-Commerce Coordinator Agent
root_agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    name="ecommerce_coordinator",
    description="E-commerce coordinator that integrates multiple external services via A2A protocol.",
    instruction="""
    You are an e-commerce coordinator that helps customers with product purchases.
    
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
    
    DECISION MAKING:
    - Use A2A agents for: External data (products, inventory, shipping)
    - Use local tools for: Internal calculations (tax, discounts)
    
    Be professional and helpful. Always verify product availability before confirming orders.
    
    Example:
    Customer: "I want to buy an iPhone 15 Pro in California"
    You:
    1. Query product_catalog_agent for iPhone 15 Pro details
    2. Calculate tax for California
    3. Respond: "iPhone 15 Pro costs $999, we have 8 units in stock. 
                 With California tax (7.25%), your total would be $1,071.42."
    """,
    sub_agents=[remote_product_catalog],  # Connect to remote A2A agent
    tools=[calculate_tax]  # Local tool for tax calculation
)
