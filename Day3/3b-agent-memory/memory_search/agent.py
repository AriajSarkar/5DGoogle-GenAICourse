"""
Day 3b Example 3: Memory Search Patterns

Demonstrates:
- Direct memory search in code (programmatic access)
- Understanding keyword matching (InMemoryMemoryService)
- Debugging and inspecting memory contents

Key Concept:
Beyond agent tools, you can search memory directly in code for debugging,
analytics, or building custom UIs. InMemoryMemoryService uses keyword matching;
production services like Vertex AI Memory Bank use semantic search.
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

# Agent for demonstrating memory search
root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="memory_search_agent",
    description="Agent for demonstrating memory search capabilities",
    instruction="""You are a helpful assistant with searchable long-term memory.
    
    Use load_memory to search your memory when users ask about past conversations.
    You can search by keywords or topics.""",
    tools=[load_memory],
)
