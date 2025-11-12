"""
Day 3a Standalone Example 1: Basic Stateful Agent

This script demonstrates how to create a session-aware agent that remembers
conversation history across multiple turns.

Concepts covered:
- InMemorySessionService for temporary session storage
- Creating and managing sessions
- Running conversations with context retention
- Understanding the difference between stateless and stateful agents

Run with:
    python Day3/3a-agent-sessions/01_stateful_agent.py
"""

import asyncio
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from utils.model_config import get_text_model


# Configuration
APP_NAME = "stateful_demo"
USER_ID = "demo_user"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


async def run_conversation():
    """Demonstrate stateful conversation with sessions."""
    
    print("=" * 60)
    print("Day 3a Example 1: Basic Stateful Agent")
    print("=" * 60)
    
    # Step 1: Create the agent
    agent = Agent(
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        name="stateful_chatbot",
        description="A chatbot that remembers conversation history",
        instruction="""You are a helpful assistant. Remember information the user 
        tells you and refer to it in future responses.""",
    )
    
    # Step 2: Create session service (temporary, in-memory storage)
    session_service = InMemorySessionService()
    
    # Step 3: Create runner with session service
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    # Step 4: Create or get session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="first_conversation",
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="first_conversation",
        )
    
    print(f"\n✅ Session created: {session.id}")
    print(f"   App: {APP_NAME}, User: {USER_ID}\n")
    
    # Step 5: Have a conversation with context retention
    queries = [
        "Hi! My name is Sam and I'm from Poland.",
        "What's my name?",  # Agent should remember from previous turn
        "Which country am I from?",  # Agent should remember this too
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'─' * 60}")
        print(f"Turn {i}")
        print(f"{'─' * 60}")
        print(f"User > {query}")
        
        # Convert query to Content format
        query_content = types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )
        
        # Stream agent response
        print(f"Agent > ", end="")
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=query_content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(text)
    
    # Step 6: Inspect session events
    print(f"\n{'=' * 60}")
    print("Session Events (Conversation History)")
    print(f"{'=' * 60}")
    
    final_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="first_conversation",
    )
    
    for i, event in enumerate(final_session.events, 1):
        if event.content and event.content.parts:
            role = event.content.role
            text = event.content.parts[0].text[:60]
            print(f"{i}. [{role}]: {text}...")
    
    print(f"\n{'=' * 60}")
    print("Key Takeaway:")
    print("The agent remembered your name and country because sessions")
    print("automatically maintain conversation history!")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(run_conversation())
