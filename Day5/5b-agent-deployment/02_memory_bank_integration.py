"""
Standalone Script: Memory Bank Integration for Long-Term Memory

This script demonstrates how to add long-term memory to your agents using Memory Bank.

KEY CONCEPTS:
- Session Memory vs Memory Bank
- PreloadMemoryTool: Automatic memory retrieval
- After-agent callback: Automatic memory saving
- InMemoryMemoryService: Local testing (dev)
- Vertex AI Memory Bank: Production (deployed)

MEMORY BANK WORKFLOW:
1. User interacts with agent (Session 1)
2. After-agent callback saves conversation to Memory Bank
3. Days/weeks later, user returns (Session 2)
4. PreloadMemoryTool automatically loads relevant memories
5. Agent uses memories to personalize response

EXAMPLE SCENARIO:
Session 1:
  User: "I prefer Celsius for temperature"
  Agent: "Got it! I'll remember that."
  → Saved to Memory Bank ✨

Session 2 (days later):
  User: "What's the weather in Tokyo?"
  Agent: (loads memory: user prefers Celsius)
  Agent: "Tokyo is clear with a temperature of 21°C."
  → No need to ask again! ✨

WHAT THIS SCRIPT DOES:
1. Creates a Memory-Enabled Weather Agent
2. Demonstrates session memory vs Memory Bank
3. Shows automatic memory save/load workflow
4. Tests cross-session recall

USAGE:
    python Day5/5b-agent-deployment/02_memory_bank_integration.py

NOTE: This script uses InMemoryMemoryService for local testing.
      When deployed to Agent Engine, Vertex AI Memory Bank is used automatically.

DEPLOYMENT WITH MEMORY BANK:
    adk deploy agent_engine Day5/5b-agent-deployment/memory_enabled_agent/ \\
        --project=your-project-id \\
        --region=us-west1
    
    # Memory Bank is automatically configured in Agent Engine
"""

import asyncio
import uuid
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import preload_memory
from google.genai import types
from utils.model_config import get_text_model


# Load environment variables
load_dotenv()


def get_weather(city: str) -> dict:
    """Get weather information for a given city."""
    weather_data = {
        "san francisco": {
            "status": "success",
            "city": "San Francisco",
            "temperature_f": 72,
            "temperature_c": 22,
            "conditions": "Sunny"
        },
        "tokyo": {
            "status": "success",
            "city": "Tokyo",
            "temperature_f": 70,
            "temperature_c": 21,
            "conditions": "Clear"
        },
        "paris": {
            "status": "success",
            "city": "Paris",
            "temperature_f": 68,
            "temperature_c": 20,
            "conditions": "Partly Cloudy"
        }
    }
    
    city_lower = city.lower()
    
    if city_lower in weather_data:
        return weather_data[city_lower]
    else:
        available = ", ".join([c.title() for c in weather_data.keys()])
        return {
            "status": "error",
            "error_message": f"Weather info for '{city}' not available. Try: {available}"
        }


# Callback to automatically save conversations to Memory Bank
async def auto_save_to_memory(callback_context):
    """
    After-agent callback that saves each conversation turn to Memory Bank.
    
    This enables cross-session recall:
    - User preferences are remembered
    - Agent can reference past conversations
    - Memory persists across sessions
    """
    memory_service = callback_context._invocation_context.memory_service
    
    if memory_service:
        session = callback_context._invocation_context.session
        await memory_service.add_session_to_memory(session)


async def run_conversation(agent, session_service, memory_service, user_id, session_id, query):
    """Run a single conversation turn."""
    
    # Create runner with BOTH session and memory services
    runner = Runner(
        agent=agent,
        app_name="weather_app",
        session_service=session_service,
        memory_service=memory_service,  # Enable Memory Bank!
    )
    
    # Create user message
    test_content = types.Content(parts=[types.Part(text=query)])
    
    print(f"👤 User: {query}")
    print(f"🤖 Agent: ", end="")
    
    # Run agent and stream response
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=test_content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text"):
                    print(part.text)


async def main():
    """
    Main function demonstrating Memory Bank integration.
    
    FLOW:
    1. Create memory-enabled agent
    2. Session 1: User sets preference (Celsius)
    3. Save session to Memory Bank
    4. Session 2: User asks about weather (NEW session)
    5. Agent loads memory and uses Celsius preference automatically
    """
    print("=" * 70)
    print("🧠 Memory Bank Integration Demo")
    print("=" * 70)
    
    # Step 1: Create services
    print("\n📦 Step 1: Setting up services...")
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()  # Local memory for testing
    
    print("   ✅ Session Service: InMemorySessionService")
    print("   ✅ Memory Service: InMemoryMemoryService (local testing)")
    print("   ℹ️  In production: Vertex AI Memory Bank is used automatically")
    
    # Step 2: Create Memory-Enabled Agent
    print("\n🤖 Step 2: Creating Memory-Enabled Weather Agent...")
    
    agent = LlmAgent(
        model=Gemini(model=get_text_model()),
        name="weather_assistant_with_memory",
        description="Weather assistant with long-term memory",
        instruction="""
        You are a friendly weather assistant with long-term memory.
        
        MEMORY CAPABILITIES:
        - Remember user preferences (temperature unit, favorite cities)
        - Recall past conversations
        - Use memories to personalize responses
        
        When users ask about weather:
        1. Use preload_memory tool to check for user preferences
        2. Use get_weather tool to fetch current weather
        3. Format response according to user's preferred temperature unit
        4. Be friendly and personalize based on remembered information
        
        PREFERENCE HANDLING:
        - If user says "I prefer Celsius", remember for future queries
        - If user says "I prefer Fahrenheit", remember for future queries
        - If no preference stored, provide both units
        
        Example:
        - Memory: User prefers Celsius
        - Query: "What's the weather in Tokyo?"
        - Response: "Tokyo is clear with a temperature of 21°C."
        """,
        tools=[
            get_weather,
            preload_memory,  # Automatically loads relevant memories
        ],
        after_agent_callback=auto_save_to_memory,  # Automatically saves memories
    )
    
    print("   ✅ Agent created with memory capabilities")
    print("   🔧 Tools: get_weather, preload_memory")
    print("   💾 Callback: auto_save_to_memory")
    
    # User and session identifiers
    user_id = "user_123"
    session_1_id = f"session_1_{uuid.uuid4().hex[:8]}"
    session_2_id = f"session_2_{uuid.uuid4().hex[:8]}"  # Different session!
    
    # Create sessions
    await session_service.create_session(
        app_name="weather_app",
        user_id=user_id,
        session_id=session_1_id
    )
    
    await session_service.create_session(
        app_name="weather_app",
        user_id=user_id,
        session_id=session_2_id
    )
    
    # Step 3: Session 1 - Set preference
    print("\n" + "=" * 70)
    print("💬 SESSION 1: Setting User Preference")
    print("=" * 70)
    print(f"Session ID: {session_1_id}")
    print()
    
    await run_conversation(
        agent, session_service, memory_service,
        user_id, session_1_id,
        "I prefer Celsius for temperature readings"
    )
    
    print("\n💾 Session 1 conversation saved to Memory Bank")
    print("   User preference 'Celsius' is now in long-term memory")
    
    # Step 4: Session 2 - New session, agent should recall preference
    print("\n" + "=" * 70)
    print("💬 SESSION 2: Testing Cross-Session Recall (NEW SESSION)")
    print("=" * 70)
    print(f"Session ID: {session_2_id} (different from Session 1!)")
    print()
    
    print("🧠 What should happen:")
    print("   1. PreloadMemoryTool loads relevant memories")
    print("   2. Agent finds 'Celsius' preference in Memory Bank")
    print("   3. Agent responds in Celsius automatically (no need to ask!)")
    print()
    
    await run_conversation(
        agent, session_service, memory_service,
        user_id, session_2_id,
        "What's the weather in Tokyo?"
    )
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ Memory Bank Integration Demo Complete!")
    print("=" * 70)
    
    print("\n📊 What Just Happened:")
    print("-" * 70)
    print("✅ Session 1:")
    print("   • User set temperature preference to Celsius")
    print("   • After-agent callback saved to Memory Bank")
    print()
    print("✅ Session 2 (NEW session, different session_id):")
    print("   • PreloadMemoryTool loaded memories automatically")
    print("   • Agent found 'Celsius' preference")
    print("   • Agent responded in Celsius without asking")
    print()
    print("✨ Key Benefit:")
    print("   User doesn't need to repeat preferences every time!")
    print("   Memories persist across sessions, days, weeks!")
    
    print("\n🔧 Technical Details:")
    print("-" * 70)
    print("Session Memory vs Memory Bank:")
    print()
    print("┌─────────────────────┬──────────────────────────────┐")
    print("│ Session Memory      │ Memory Bank                  │")
    print("├─────────────────────┼──────────────────────────────┤")
    print("│ Single conversation │ All conversations            │")
    print("│ Forgets when ends   │ Remembers permanently        │")
    print("│ \"What did I say?\"   │ \"What's my favorite city?\"  │")
    print("│ Auto-enabled        │ Requires setup               │")
    print("└─────────────────────┴──────────────────────────────┘")
    
    print("\n💡 Production Deployment:")
    print("-" * 70)
    print("When deployed to Agent Engine:")
    print("• InMemoryMemoryService → Vertex AI Memory Bank")
    print("• LLM-powered consolidation (not just keyword matching)")
    print("• Semantic search (finds related memories)")
    print("• Auto-scaling (handles large memory databases)")
    print()
    print("Deploy command:")
    print("  adk deploy agent_engine memory_enabled_agent/ \\")
    print("      --project=your-project-id \\")
    print("      --region=us-west1")
    
    print("\n📚 Learn More:")
    print("-" * 70)
    print("• ADK Memory Guide:")
    print("  https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/memory")
    print("• Memory Tools:")
    print("  https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/memory-tools")
    print("• Vertex AI Memory Bank:")
    print("  https://cloud.google.com/vertex-ai/docs/memory-bank")


if __name__ == "__main__":
    asyncio.run(main())
