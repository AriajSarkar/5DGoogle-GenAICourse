"""
Day 3a Standalone Example 2: Persistent Sessions with Database

This script demonstrates how to use DatabaseSessionService to persist
sessions across application restarts.

Concepts covered:
- DatabaseSessionService with SQLite
- Session persistence (survives restarts)
- Session isolation between different session IDs
- Inspecting database contents

Run with:
    python Day3/3a-agent-sessions/02_persistent_sessions.py
    
Try it:
    1. Run this script
    2. Stop the script (Ctrl+C)
    3. Run it again - the conversation history is still there!
"""

import asyncio
import sqlite3
import os
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from utils.model_config import get_text_model


APP_NAME = "persistent_demo"
USER_ID = "demo_user"
DB_FILE = "sessions_demo.db"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


async def run_persistent_session():
    """Demonstrate persistent sessions with database storage."""
    
    print("=" * 60)
    print("Day 3a Example 2: Persistent Sessions")
    print("=" * 60)
    
    # Step 1: Create agent
    agent = LlmAgent(
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        name="persistent_chatbot",
        description="A chatbot with persistent session storage",
        instruction="""You are a helpful assistant. Remember what users tell you.""",
    )
    
    # Step 2: Create DatabaseSessionService (persists to SQLite)
    db_url = f"sqlite:///{DB_FILE}"
    session_service = DatabaseSessionService(db_url=db_url)
    
    print(f"\n✅ Using persistent storage: {DB_FILE}")
    
    # Step 3: Create runner
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    # Step 4: Create/get session for Test 1
    print("\n" + "─" * 60)
    print("Test 1: First Conversation (session-01)")
    print("─" * 60)
    
    try:
        session1 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="session-01",
        )
    except:
        session1 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="session-01",
        )
    
    # First conversation
    queries_1 = [
        "Hi, I'm Sam from Poland. My favorite color is blue.",
        "What's my name?",
    ]
    
    for query in queries_1:
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
    
    # Step 5: Verify persistence - query the database
    print("\n" + "─" * 60)
    print("Database Contents")
    print("─" * 60)
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT app_name, session_id, author FROM events"
        )
        
        print(f"\n{'App':<20} {'Session ID':<15} {'Author':<20}")
        print("─" * 60)
        for row in result.fetchall():
            print(f"{row[0]:<20} {row[1]:<15} {row[2]:<20}")
    
    # Step 6: Test session isolation - different session ID
    print("\n" + "─" * 60)
    print("Test 2: New Session (session-02) - Should NOT know name")
    print("─" * 60)
    
    try:
        session2 = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="session-02",  # Different session ID!
        )
    except:
        session2 = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="session-02",
        )
    
    query = "What's my name?"
    print(f"\nUser > {query}")
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("Agent > ", end="")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session2.id,
        new_message=query_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                print(text)
    
    # Step 7: Resume original session
    print("\n" + "─" * 60)
    print("Test 3: Resume Original Session (session-01)")
    print("─" * 60)
    
    query = "What's my favorite color?"
    print(f"\nUser > {query}")
    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    
    print("Agent > ", end="")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session1.id,  # Back to original session!
        new_message=query_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text != "None":
                print(text)
    
    print(f"\n{'=' * 60}")
    print("Key Takeaways:")
    print("1. DatabaseSessionService persists sessions to disk")
    print("2. Sessions survive application restarts")
    print("3. Different session IDs have isolated histories")
    print("4. You can resume any session using its session_id")
    print(f"{'=' * 60}\n")
    
    print(f"💡 Try: Stop and restart this script - session-01 is still there!")
    print(f"📂 Database file: {DB_FILE}\n")


if __name__ == "__main__":
    asyncio.run(run_persistent_session())
