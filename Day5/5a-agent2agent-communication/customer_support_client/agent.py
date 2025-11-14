"""
Customer Support Client Agent (A2A Consumer)

This agent demonstrates how to CONSUME a remote agent via Agent2Agent (A2A) Protocol.

KEY CONCEPTS:
- RemoteA2aAgent: Client-side proxy that connects to A2A server
- Agent Card Discovery: Reads capabilities from /.well-known/agent-card.json
- Transparent Communication: Use remote agent like a local sub-agent
- Protocol Translation: ADK handles HTTP/JSON communication

ARCHITECTURE:
This agent represents your internal customer support system.
It consumes the Product Catalog Agent (external vendor) via A2A protocol.

PREREQUISITES:
1. Start Product Catalog Server first:
   python Day5/5a-agent2agent-communication/01_a2a_server.py
   
2. Verify agent card is accessible:
   curl http://localhost:8001/.well-known/agent-card.json

RUN WITH:
    adk run Day5/5a-agent2agent-communication/customer_support_client/
    
    # Then ask: "What's the price of iPhone 15 Pro?"
    # The agent will call the remote Product Catalog Agent via A2A!
"""

from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.models.google_llm import Gemini
from utils.model_config import get_text_model


# Create a RemoteA2aAgent that connects to the Product Catalog Server
# This acts as a client-side proxy - customer support can use it like a local sub-agent
remote_product_catalog_agent = RemoteA2aAgent(
    name="product_catalog_agent",
    description="Remote product catalog agent from external vendor that provides product information.",
    # Point to the agent card URL - ADK reads this to discover capabilities
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
)


# Create the Customer Support Agent that uses the remote Product Catalog Agent
root_agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    name="customer_support_agent",
    description="A customer support assistant that helps customers with product inquiries and information.",
    instruction="""
    You are a friendly and professional customer support agent.
    
    When customers ask about products:
    1. Use the product_catalog_agent sub-agent to look up product information
    2. Provide clear answers about pricing, availability, and specifications
    3. If a product is out of stock, mention the expected availability
    4. Be helpful and professional
    
    IMPORTANT: Always get product information from the product_catalog_agent before answering.
    Do not make up product details or prices - always use the catalog agent.
    
    Example workflow:
    - Customer: "What's the price of iPhone 15 Pro?"
    - You: Use product_catalog_agent to get info
    - You: "The iPhone 15 Pro costs $999 and we have low stock (8 units). It features 128GB storage and a titanium finish."
    """,
    sub_agents=[remote_product_catalog_agent]  # Add the remote agent as a sub-agent!
)
