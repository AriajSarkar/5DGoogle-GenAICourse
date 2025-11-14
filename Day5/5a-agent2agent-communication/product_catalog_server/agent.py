"""
Product Catalog Server Agent (A2A Provider)

This agent demonstrates how to EXPOSE an ADK agent via Agent2Agent (A2A) Protocol.

KEY CONCEPTS:
- to_a2a(): Converts any ADK agent into an A2A-compatible server
- Agent Card: Auto-generated JSON describing agent capabilities
- Standard endpoint: /.well-known/agent-card.json
- FastAPI/Starlette: Handles A2A protocol communication

ARCHITECTURE:
This agent represents an external vendor's product catalog system.
Other agents (like customer support) can consume it via A2A protocol.

RUN WITH:
    adk run Day5/5a-agent2agent-communication/product_catalog_server/

EXPOSE AS A2A SERVER:
    python Day5/5a-agent2agent-communication/01_a2a_server.py
    (Then query agent card at http://localhost:8001/.well-known/agent-card.json)
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from utils.model_config import get_text_model


def get_product_info(product_name: str) -> dict:
    """
    Get product information for a given product.
    
    This is a TOOL that becomes a "skill" in the A2A agent card.
    Other agents can discover and use this capability via A2A protocol.
    
    Args:
        product_name: Name of the product (e.g., "iPhone 15 Pro", "MacBook Pro")
    
    Returns:
        dict: Product information with status, or error if not found
    """
    # Mock product catalog - in production, this would query a real database
    product_catalog = {
        "iphone 15 pro": {
            "status": "success",
            "product": "iPhone 15 Pro",
            "price": "$999",
            "stock": "Low Stock (8 units)",
            "specs": "128GB, Titanium finish"
        },
        "samsung galaxy s24": {
            "status": "success",
            "product": "Samsung Galaxy S24",
            "price": "$799",
            "stock": "In Stock (31 units)",
            "specs": "256GB, Phantom Black"
        },
        "dell xps 15": {
            "status": "success",
            "product": "Dell XPS 15",
            "price": "$1,299",
            "stock": "In Stock (45 units)",
            "specs": '15.6" display, 16GB RAM, 512GB SSD'
        },
        "macbook pro 14": {
            "status": "success",
            "product": 'MacBook Pro 14"',
            "price": "$1,999",
            "stock": "In Stock (22 units)",
            "specs": "M3 Pro chip, 18GB RAM, 512GB SSD"
        },
        "sony wh-1000xm5": {
            "status": "success",
            "product": "Sony WH-1000XM5 Headphones",
            "price": "$399",
            "stock": "In Stock (67 units)",
            "specs": "Noise-canceling, 30hr battery"
        },
        "ipad air": {
            "status": "success",
            "product": "iPad Air",
            "price": "$599",
            "stock": "In Stock (28 units)",
            "specs": '10.9" display, 64GB'
        },
        "lg ultrawide 34": {
            "status": "success",
            "product": 'LG UltraWide 34" Monitor',
            "price": "$499",
            "stock": "Out of Stock",
            "specs": "Expected: Next week"
        }
    }
    
    product_lower = product_name.lower().strip()
    
    if product_lower in product_catalog:
        return product_catalog[product_lower]
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have information for '{product_name}'. Available products: {available}"
        }


# Create the Product Catalog Agent
# This agent will be exposed via A2A protocol using to_a2a()
root_agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    name="product_catalog_agent",
    description="External vendor's product catalog agent that provides product information and availability.",
    instruction="""
    You are a product catalog specialist from an external vendor.
    
    When asked about products:
    1. Use the get_product_info tool to fetch data from the catalog
    2. Provide clear, accurate product information including price, availability, and specs
    3. If asked about multiple products, look up each one
    4. Be professional and helpful
    
    Always structure your responses with:
    - Product name
    - Price
    - Availability status
    - Key specifications
    """,
    tools=[get_product_info]
)
