"""
Day 3a Example 1: Basic Stateful Agent

Demonstrates:
- Creating a session-aware agent with InMemorySessionService
- Understanding conversation continuity across turns
- How sessions maintain context automatically

Key Concept:
Without sessions, LLMs are stateless - they forget everything after each response.
With sessions, the agent remembers the entire conversation history.
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from utils.model_config import get_text_model
from google.genai import types

# Configure retry options for API resilience
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Create a basic agent
# Note: This is just the agent definition - sessions are managed by the Runner
root_agent = Agent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="stateful_chatbot",
    description="A chatbot that remembers conversation history using sessions",
    instruction="""You are a helpful assistant. Remember information the user tells you 
    and refer to it in future responses. Be conversational and friendly.""",
)
