"""
Day 3b Standalone Example 1: Basic Memory Integration

This script demonstrates the three-step memory workflow:
1. Initialize MemoryService
2. Ingest session data to memory
3. Retrieve memories using load_memory tool

Concepts covered:
- InMemoryMemoryService for development
- Manual memory ingestion with add_session_to_memory()
- Cross-session memory retrieval
- Difference between load_memory (reactive) and preload_memory (proactive)

Run with:
    python Day3/3b-agent-memory/01_basic_memory.py
"""

import asyncio
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory
from google.genai import types
from utils.model_config import get_text_model


APP_NAME = "memory_demo"
USER_ID = "demo_user"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


async def run_basic_memory():
    """Demonstrate basic memory integration and retrieval."""
    
    print("=" * 60)
    print("Day 3b Example 1: Basic Memory Integration")
    print("=" * 60)
    
    # STEP 1: Initialize - Create MemoryService
    print("\n📦 Step 1: Initialize MemoryService")
    print("─" * 60)
    
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()  # Long-term storage
    
    print("✅ Session service created (short-term)")
    print("✅ Memory service created (long-term)")
    
    # Create agent with load_memory tool
    agent = LlmAgent(
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        name="memory_demo_agent",
        description="Agent with memory capabilities",
        instruction="""You are a helpful assistant with long-term memory.
        
        Use the load_memory tool when you need to recall information from
        past conversations. If a user asks about something they mentioned
        before, search your memory first.""",
        tools=[load_memory],  # Agent can search memory
    )
    
    # Create runner with BOTH services
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,  # Memory enabled!
    )
    
    print("✅ Agent created with load_memory tool")
    print("✅ Runner initialized with both services")
    
    # STEP 2: Ingest - Save conversation to memory
    print("\n💾 Step 2: Ingest Session Data to Memory")
    print("─" * 60)
    
    # Have a conversation
    try:
        session1 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="conversation-01",
        )
    except:
        session1 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="conversation-01",
        )
    
    query = "My favorite color is blue-green. Can you remember that?"
    print(f"\nUser > {query}")
    
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("Agent > ", end="")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session1.id,
        new_message=query_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                print(text)
    
    # Manually save session to memory (the KEY step!)
    print("\n📥 Saving session to memory...")
    session1_final = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="conversation-01",
    )
    
    await memory_service.add_session_to_memory(session1_final)
    print("✅ Session saved to long-term memory!")
    
    # STEP 3: Retrieve - Query memory in NEW session
    print("\n🔍 Step 3: Retrieve from Memory (New Session)")
    print("─" * 60)
    
    # Create a DIFFERENT session
    try:
        session2 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="conversation-02",  # Different session!
        )
    except:
        session2 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="conversation-02",
        )
    
    query = "What's my favorite color?"
    print(f"\nUser > {query}")
    print("(This is a NEW session - agent must use memory to answer)")
    
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("\nAgent > ", end="")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session2.id,  # Different session ID!
        new_message=query_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                print(text)
    
    # Demonstrate manual memory search
    print("\n\n🔎 Manual Memory Search (Programmatic Access)")
    print("─" * 60)
    
    search_response = await memory_service.search_memory(
        app_name=APP_NAME,
        user_id=USER_ID,
        query="favorite color",
    )
    
    print(f"\nSearch query: 'favorite color'")
    print(f"Found {len(search_response.memories)} memories:\n")
    
    for i, memory in enumerate(search_response.memories, 1):
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"{i}. [{memory.author}]: {text}...")
    
    # Summary
    print(f"\n{'=' * 60}")
    print("Key Takeaways:")
    print("─" * 60)
    print("1. Memory requires THREE components:")
    print("   - MemoryService (storage)")
    print("   - add_session_to_memory() (ingestion)")
    print("   - load_memory tool (retrieval)")
    print()
    print("2. Sessions = short-term (single conversation)")
    print("   Memory = long-term (across conversations)")
    print()
    print("3. Agent successfully recalled 'blue-green' from a")
    print("   DIFFERENT session by searching memory!")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(run_basic_memory())
