"""
Day 3b Standalone Example 3: Memory Consolidation Concepts

This script demonstrates the concept of memory consolidation - how raw
conversation events are transformed into concise, searchable facts.

Note: InMemoryMemoryService stores raw events WITHOUT consolidation.
Production services like Vertex AI Memory Bank (Day 5) perform LLM-powered
consolidation automatically.

Concepts covered:
- The problem with raw storage (token explosion)
- Conceptual overview of consolidation
- Keyword matching vs semantic search
- Direct memory search API

Run with:
    python Day3/3b-agent-memory/03_memory_consolidation.py
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


APP_NAME = "consolidation_demo"
USER_ID = "demo_user"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


async def run_consolidation_demo():
    """Demonstrate memory consolidation concepts."""
    
    print("=" * 60)
    print("Day 3b Example 3: Memory Consolidation Concepts")
    print("=" * 60)
    
    # Initialize services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    agent = LlmAgent(
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        name="consolidation_demo_agent",
        description="Agent for demonstrating memory search",
        instruction="""You are a helpful assistant. Answer user questions.""",
        tools=[load_memory],
    )
    
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )
    
    # The Problem: Verbose conversations
    print("\n📊 THE PROBLEM: Raw Storage Token Explosion")
    print("─" * 60)
    
    try:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="verbose-conv",
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id="verbose-conv",
        )
    
    # Simulate a verbose conversation about allergies
    verbose_queries = [
        "I'm allergic to peanuts.",
        "Oh, and I can't eat tree nuts either.",
        "Basically anything with nuts is bad for me.",
        "Thanks for noting that!",
    ]
    
    print("\nVerbose conversation (stored in full):\n")
    
    for i, query in enumerate(verbose_queries, 1):
        print(f"{i}. User > {query}")
        
        query_content = types.Content(role="user", parts=[types.Part(text=query)])
        
        print(f"   Agent > ", end="")
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
    
    # Save to memory (stores ALL messages)
    final_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id="verbose-conv",
    )
    
    await memory_service.add_session_to_memory(final_session)
    
    print("💾 Saved to InMemoryMemoryService (NO consolidation)")
    print(f"   Stored: {len(final_session.events)} raw events")
    
    # Show what's actually stored
    print("\n📝 What's Stored in Memory (Raw Events):")
    print("─" * 60)
    
    for i, event in enumerate(final_session.events, 1):
        if event.content and event.content.parts:
            role = event.content.role
            text = event.content.parts[0].text[:50]
            print(f"{i}. [{role}]: {text}...")
    
    # The Ideal: Consolidated memory
    print("\n\n✨ IDEAL: Consolidated Memory (Conceptual)")
    print("─" * 60)
    print("\nWhat a consolidation service WOULD extract:")
    print()
    print("  Extracted Memory:")
    print('  {')
    print('    "allergy": "peanuts, tree nuts",')
    print('    "severity": "avoid completely",')
    print('    "category": "food"')
    print('  }')
    print()
    print("  → 1 concise fact instead of 8 verbose messages!")
    
    # Test keyword search
    print("\n\n🔍 SEARCH: Keyword Matching (InMemoryMemoryService)")
    print("─" * 60)
    
    # Test different queries
    test_queries = [
        "allergic",  # Should match
        "peanuts",  # Should match
        "nuts",  # Should match
        "food restrictions",  # Won't match (different words)
        "dietary limitations",  # Won't match (synonyms not recognized)
    ]
    
    for query in test_queries:
        search_response = await memory_service.search_memory(
            app_name=APP_NAME,
            user_id=USER_ID,
            query=query,
        )
        
        match_status = "✅ Match" if search_response.memories else "❌ No match"
        match_count = len(search_response.memories)
        print(f"\nQuery: '{query}'")
        print(f"  {match_status} ({match_count} memories found)")
        
        if search_response.memories:
            # Show first matching memory
            first_match = search_response.memories[0]
            if first_match.content and first_match.content.parts:
                text = first_match.content.parts[0].text[:60]
                print(f"  Example: {text}...")
    
    # Comparison with production service
    print(f"\n\n{'=' * 60}")
    print("InMemoryMemoryService vs Production (Conceptual)")
    print(f"{'=' * 60}")
    
    print("\n┌─────────────────────┬──────────────────┬─────────────────┐")
    print("│ Feature             │ InMemory         │ Vertex AI       │")
    print("├─────────────────────┼──────────────────┼─────────────────┤")
    print("│ Storage             │ Raw events       │ Consolidated    │")
    print("│ Search method       │ Keyword matching │ Semantic search │")
    print("│ Consolidation       │ None             │ LLM-powered     │")
    print("│ Persistence         │ In-memory only   │ Cloud storage   │")
    print("│ Token efficiency    │ Low              │ High            │")
    print("└─────────────────────┴──────────────────┴─────────────────┘")
    
    print("\n\n📚 Key Takeaways:")
    print("─" * 60)
    print("1. Raw storage = Verbose, expensive, slow")
    print("   Consolidation = Concise, efficient, fast")
    print()
    print("2. InMemoryMemoryService (this example):")
    print("   - Stores raw events")
    print("   - Keyword matching only")
    print("   - Good for learning, not production")
    print()
    print("3. Vertex AI Memory Bank (Day 5):")
    print("   - LLM-powered consolidation")
    print("   - Semantic search (understands meaning)")
    print("   - Production-ready")
    print()
    print("4. Same API for both!")
    print("   - add_session_to_memory()")
    print("   - search_memory()")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    asyncio.run(run_consolidation_demo())
