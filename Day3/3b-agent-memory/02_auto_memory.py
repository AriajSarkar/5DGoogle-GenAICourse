"""
Day 3b Standalone Example 2: Automated Memory with Callbacks

This script demonstrates how to use callbacks to automatically save sessions
to memory after every turn, eliminating manual intervention.

Concepts covered:
- Using after_agent_callback for automatic memory saving
- Combining callbacks with preload_memory for full automation
- Understanding callback_context and lifecycle hooks
- Zero-manual-intervention memory systems

Run with:
    python Day3/3b-agent-memory/02_auto_memory.py
"""

import asyncio
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import preload_memory
from google.genai import types
from utils.model_config import get_text_model


APP_NAME = "auto_memory_demo"
USER_ID = "demo_user"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# Callback to automatically save sessions to memory
async def auto_save_to_memory(callback_context):
    """
    Automatically save session to memory after each agent turn.
    
    This callback is triggered after every agent response.
    The callback_context provides access to the memory service and session.
    """
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


async def run_auto_memory():
    """Demonstrate fully automated memory management."""
    
    print("=" * 60)
    print("Day 3b Example 2: Automated Memory with Callbacks")
    print("=" * 60)
    
    # Initialize services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    # Create agent with automatic memory saving and loading
    agent = LlmAgent(
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        name="auto_memory_agent",
        description="Agent with fully automated memory",
        instruction="""You are a helpful assistant with automated long-term memory.
        
        Your conversations are automatically saved and loaded, so you always
        have access to past information without manual intervention.""",
        tools=[preload_memory],  # Proactive: always loads memory
        after_agent_callback=auto_save_to_memory,  # Automatic saving!
    )
    
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )
    
    print("\n✅ Agent configured with:")
    print("   - preload_memory (automatic retrieval)")
    print("   - after_agent_callback (automatic saving)")
    
    # Test 1: First conversation
    print("\n" + "─" * 60)
    print("Test 1: First Conversation")
    print("─" * 60)
    
    try:
        session1 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-01",
        )
    except:
        session1 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-01",
        )
    
    query = "My birthday is March 15th. Please remember this!"
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
    
    print("\n💡 Callback automatically saved this to memory!")
    
    # Test 2: Second conversation (different session)
    print("\n" + "─" * 60)
    print("Test 2: New Session - Memory Retrieval")
    print("─" * 60)
    
    try:
        session2 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-02",  # Different session!
        )
    except:
        session2 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-02",
        )
    
    query = "When is my birthday?"
    print(f"\nUser > {query}")
    print("(New session - preload_memory should automatically retrieve)")
    
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("\nAgent > ", end="")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session2.id,
        new_message=query_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                print(text)
    
    print("\n💡 preload_memory automatically loaded the memory!")
    
    # Test 3: Third conversation - add more info
    print("\n" + "─" * 60)
    print("Test 3: Adding More Information")
    print("─" * 60)
    
    try:
        session3 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-03",
        )
    except:
        session3 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-03",
        )
    
    query = "I also like pizza with pineapple!"
    print(f"\nUser > {query}")
    
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("Agent > ", end="")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session3.id,
        new_message=query_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                print(text)
    
    print("\n💡 This is also automatically saved!")
    
    # Test 4: Fourth conversation - recall everything
    print("\n" + "─" * 60)
    print("Test 4: Recall Multiple Memories")
    print("─" * 60)
    
    try:
        session4 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-04",
        )
    except:
        session4 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="auto-conv-04",
        )
    
    query = "What do you know about me?"
    print(f"\nUser > {query}")
    
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("Agent > ", end="")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session4.id,
        new_message=query_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                print(text)
    
    # Summary
    print(f"\n\n{'=' * 60}")
    print("Key Takeaways:")
    print("─" * 60)
    print("1. Callbacks eliminate manual add_session_to_memory() calls")
    print()
    print("2. after_agent_callback runs after every agent turn")
    print("   - Automatically saves conversation to memory")
    print()
    print("3. preload_memory vs load_memory:")
    print("   - preload_memory: Proactive (always loads)")
    print("   - load_memory: Reactive (agent decides when)")
    print()
    print("4. Fully automated memory = callbacks + preload_memory")
    print("   - Zero manual intervention")
    print("   - Memory always available")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(run_auto_memory())
