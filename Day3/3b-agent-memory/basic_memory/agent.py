"""
Day 3b Example 1: Basic Memory Integration

Demonstrates:
- Initializing InMemoryMemoryService
- Manual memory ingestion with add_session_to_memory()
- Cross-session memory retrieval
- Difference between load_memory and preload_memory tools

Key Concept:
Memory is long-term storage across conversations. Sessions are short-term.
Agent needs memory tools (load_memory or preload_memory) to retrieve memories.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import load_memory
from utils.model_config import get_text_model
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Agent with load_memory tool (reactive pattern)
root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="memory_demo_agent",
    description="Agent demonstrating basic memory functionality",
    instruction="""You are a helpful assistant with long-term memory.
    
    Use the load_memory tool when you need to recall information from past conversations.
    If a user asks about something they mentioned before (even in different sessions),
    search your memory first before saying you don't know.""",
    tools=[load_memory],  # Agent can search memory when needed
)
