"""
Standalone Script: Exposing an Agent via A2A Protocol

This script demonstrates how to expose an ADK agent as an A2A-compatible server.

KEY CONCEPTS:
- to_a2a(): Converts any ADK agent into A2A server (FastAPI/Starlette app)
- Agent Card: Auto-generated JSON at /.well-known/agent-card.json
- uvicorn: ASGI server that runs the A2A app
- Background Process: Server runs independently, accepts requests from other agents

WHAT THIS SCRIPT DOES:
1. Creates a Product Catalog Agent with get_product_info tool
2. Wraps it with to_a2a() to make it A2A-compatible
3. Starts a uvicorn server in the background on port 8001
4. Serves the agent card at http://localhost:8001/.well-known/agent-card.json
5. Accepts A2A protocol requests at http://localhost:8001/tasks

USAGE:
    # Start the A2A server (runs in background)
    python Day5/5a-agent2agent-communication/01_a2a_server.py
    
    # In another terminal, query the agent card:
    curl http://localhost:8001/.well-known/agent-card.json
    
    # Or connect a consumer agent (see 02_a2a_client.py)

CLEANUP:
    # Stop the server (find PID and kill)
    ps aux | grep uvicorn
    kill <PID>

PRODUCTION DEPLOYMENT:
In production, you'd deploy this to:
- Cloud Run: adk deploy cloud_run product_catalog_server/
- Agent Engine: adk deploy agent_engine product_catalog_server/
- GKE: adk deploy gke product_catalog_server/

For this learning script, we run locally with uvicorn.
"""

import asyncio
import os
import subprocess
import time
import requests
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from utils.model_config import get_text_model


# Load environment variables
load_dotenv()


def get_product_info(product_name: str) -> dict:
    """Get product information for a given product."""
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
    }
    
    product_lower = product_name.lower().strip()
    
    if product_lower in product_catalog:
        return product_catalog[product_lower]
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have information for '{product_name}'. Available: {available}"
        }


async def main():
    """
    Main function to start the A2A server.
    
    FLOW:
    1. Create Product Catalog Agent
    2. Convert to A2A app using to_a2a()
    3. Write server code to temporary file
    4. Start uvicorn server in background
    5. Wait for server to be ready
    6. Display server information
    """
    print("=" * 60)
    print("🚀 Starting A2A Product Catalog Server")
    print("=" * 60)
    
    # Step 1: Create the Product Catalog Agent
    print("\n📦 Step 1: Creating Product Catalog Agent...")
    product_catalog_agent = LlmAgent(
        model=Gemini(model=get_text_model()),
        name="product_catalog_agent",
        description="External vendor's product catalog agent that provides product information and availability.",
        instruction="""
        You are a product catalog specialist from an external vendor.
        When asked about products, use the get_product_info tool to fetch data from the catalog.
        Provide clear, accurate product information including price, availability, and specs.
        Be professional and helpful.
        """,
        tools=[get_product_info]
    )
    print("   ✅ Agent created with get_product_info tool")
    
    # Step 2: Convert to A2A app
    print("\n🌐 Step 2: Converting agent to A2A-compatible server...")
    product_catalog_a2a_app = to_a2a(
        product_catalog_agent,
        port=8001  # Port where this agent will be served
    )
    print("   ✅ Agent wrapped with to_a2a()")
    print("   📋 Auto-generated agent card at /.well-known/agent-card.json")
    
    # Step 3: Write server code to temporary file (for uvicorn)
    print("\n📝 Step 3: Creating server script...")
    
    server_code = '''
import os
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini

def get_product_info(product_name: str) -> dict:
    """Get product information for a given product."""
    product_catalog = {
        "iphone 15 pro": {"status": "success", "product": "iPhone 15 Pro", "price": "$999", "stock": "Low Stock (8 units)", "specs": "128GB, Titanium finish"},
        "samsung galaxy s24": {"status": "success", "product": "Samsung Galaxy S24", "price": "$799", "stock": "In Stock (31 units)", "specs": "256GB, Phantom Black"},
        "dell xps 15": {"status": "success", "product": "Dell XPS 15", "price": "$1,299", "stock": "In Stock (45 units)", "specs": "15.6\\" display, 16GB RAM, 512GB SSD"},
    }
    
    product_lower = product_name.lower().strip()
    if product_lower in product_catalog:
        return product_catalog[product_lower]
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return {"status": "error", "error_message": f"Sorry, no info for '{product_name}'. Available: {available}"}

product_catalog_agent = LlmAgent(
    model=Gemini(model=os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash-lite")),
    name="product_catalog_agent",
    description="External vendor's product catalog agent that provides product information and availability.",
    instruction="You are a product catalog specialist. Use get_product_info tool to fetch data. Be professional.",
    tools=[get_product_info]
)

# Create the A2A app
app = to_a2a(product_catalog_agent, port=8001)
'''
    
    # Write to temporary file
    temp_dir = os.path.join(os.getcwd(), ".temp_a2a")
    os.makedirs(temp_dir, exist_ok=True)
    server_file = os.path.join(temp_dir, "product_catalog_server.py")
    
    with open(server_file, "w") as f:
        f.write(server_code)
    
    print(f"   ✅ Server script written to {server_file}")
    
    # Step 4: Start uvicorn server in background
    print("\n🚀 Step 4: Starting uvicorn server...")
    print("   Command: uvicorn product_catalog_server:app --host localhost --port 8001")
    
    server_process = subprocess.Popen(
        [
            "uvicorn",
            "product_catalog_server:app",
            "--host", "localhost",
            "--port", "8001"
        ],
        cwd=temp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ}  # Pass environment variables (including GOOGLE_API_KEY)
    )
    
    # Step 5: Wait for server to be ready
    print("\n⏳ Step 5: Waiting for server to be ready...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8001/.well-known/agent-card.json", timeout=1)
            if response.status_code == 200:
                print("   ✅ Server is ready!\n")
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        print("\n   ⚠️ Server may not be ready yet. Check manually if needed.")
        return
    
    # Step 6: Display server information
    print("=" * 60)
    print("✅ A2A Product Catalog Server is Running!")
    print("=" * 60)
    print(f"\n📍 Server URL: http://localhost:8001")
    print(f"📋 Agent Card: http://localhost:8001/.well-known/agent-card.json")
    print(f"🔧 Task Endpoint: http://localhost:8001/tasks (POST)")
    print(f"\n🔍 View Agent Card:")
    print("   curl http://localhost:8001/.well-known/agent-card.json | jq .")
    print(f"\n🎧 Connect Consumer Agent:")
    print("   python Day5/5a-agent2agent-communication/02_a2a_client.py")
    print(f"\n🛑 Stop Server:")
    print("   1. Find process: ps aux | grep uvicorn")
    print("   2. Kill process: kill <PID>")
    print("   (Or press Ctrl+C if running in foreground)")
    
    # Fetch and display agent card
    print("\n📋 Agent Card Contents:")
    print("-" * 60)
    try:
        response = requests.get("http://localhost:8001/.well-known/agent-card.json", timeout=5)
        if response.status_code == 200:
            import json
            agent_card = response.json()
            print(json.dumps(agent_card, indent=2))
            print("-" * 60)
            print(f"\n✨ Key Information:")
            print(f"   Name: {agent_card.get('name')}")
            print(f"   Description: {agent_card.get('description')}")
            print(f"   Protocol Version: {agent_card.get('protocolVersion')}")
            print(f"   Skills: {len(agent_card.get('skills', []))} capabilities")
    except Exception as e:
        print(f"⚠️ Could not fetch agent card: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Server setup complete!")
    print("=" * 60)
    print("\nℹ️  Server is running in the background.")
    print("   You can now connect consumer agents to this A2A server.")
    print("   Press Ctrl+C to exit this script (server will keep running).")
    
    # Keep script running to show logs (optional)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Exiting script. Server is still running in background.")
        print("   Remember to stop the uvicorn process manually!")


if __name__ == "__main__":
    asyncio.run(main())
