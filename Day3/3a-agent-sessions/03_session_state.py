"""
Day 3a Standalone Example 3: Session State Management

This script demonstrates how to use session state to share structured data
across conversation turns using custom tools.

Concepts covered:
- Creating tools that read/write session state
- Using ToolContext to access session state
- State scope prefixes (user:, app:, temp:)
- Sharing data without re-asking users

Run with:
    python Day3/3a-agent-sessions/03_session_state.py
"""

import asyncio
from typing import Dict, Any
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from utils.model_config import get_text_model


APP_NAME = "session_state_demo"
USER_ID = "demo_user"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# Tool 1: Save user information to session state
def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """
    Record and save user name and country in session state.
    
    Args:
        user_name: The user's name to store
        country: The user's country to store
    
    Returns:
        Status dictionary indicating success
    """
    # Write to session state using 'user:' prefix
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country
    
    return {
        "status": "success",
        "message": f"Saved {user_name} from {country} to session state",
    }


# Tool 2: Retrieve user information from session state
def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieve user name and country from session state.
    
    Returns:
        Dictionary with user_name and country
    """
    # Read from session state
    user_name = tool_context.state.get("user:name", "Username not found")
    country = tool_context.state.get("user:country", "Country not found")
    
    return {
        "status": "success",
        "user_name": user_name,
        "country": country,
    }


async def run_session_state_demo():
    """Demonstrate session state management with custom tools."""
    
    print("=" * 60)
    print("Day 3a Example 3: Session State Management")
    print("=" * 60)
    
    # Step 1: Create agent with state management tools
    agent = LlmAgent(
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        name="state_demo_agent",
        description="Agent demonstrating session state",
        instruction="""You are a helpful assistant with tools for managing user information.
        
        Tools for managing user context:
        - Use `save_userinfo` when the user provides their name and country
        - Use `retrieve_userinfo` when you need to recall stored information
        
        When the user introduces themselves, immediately save their information.
        When asked about their details later, retrieve from session state.""",
        tools=[save_userinfo, retrieve_userinfo],
    )
    
    # Step 2: Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    # Step 3: Create session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="state_test",
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="state_test",
        )
    
    print(f"\n✅ Session created: {session.id}\n")
    
    # Step 4: Conversation demonstrating state management
    queries = [
        "Hi there! What's my name?",  # Should not know yet
        "My name is Sam and I'm from Poland.",  # Should save to state
        "What's my name?",  # Should retrieve from state
        "Which country am I from?",  # Should retrieve from state
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"{'─' * 60}")
        print(f"Turn {i}")
        print(f"{'─' * 60}")
        print(f"User > {query}")
        
        query_content = types.Content(role="user", parts=[types.Part(text=query)])
        
        print("Agent > ", end="")
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=query_content,
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(text)
        
        print()
    
    # Step 5: Inspect session state
    print(f"{'=' * 60}")
    print("Session State Contents")
    print(f"{'=' * 60}")
    
    final_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="state_test",
    )
    
    print(f"\n{final_session.state}\n")
    
    print(f"{'=' * 60}")
    print("Key Takeaways:")
    print("1. Tools can write to session state via tool_context.state")
    print("2. Use prefixes like 'user:' to organize state keys")
    print("3. State persists across turns in the same session")
    print("4. State is isolated per session (not shared)")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(run_session_state_demo())
