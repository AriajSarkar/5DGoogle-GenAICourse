"""
Day 3a Example 2: Persistent Sessions with Database Storage

Demonstrates:
- Using DatabaseSessionService for persistent storage
- Sessions that survive application restarts
- Understanding session isolation between users

Key Concept:
InMemorySessionService loses data on restart. DatabaseSessionService persists
sessions to SQLite/Postgres, enabling conversation resumption across restarts.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from utils.model_config import get_text_model
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Create agent - same as before, but runner will use DatabaseSessionService
root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="persistent_chatbot",
    description="A chatbot with persistent session storage",
    instruction="""You are a helpful assistant with persistent memory.
    You can remember conversations even after the application restarts.""",
)
