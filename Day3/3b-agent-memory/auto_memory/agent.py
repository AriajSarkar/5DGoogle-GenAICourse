"""
Day 3b Example 2: Automated Memory with Callbacks

Demonstrates:
- Using after_agent_callback for automatic memory saving
- Combining callbacks with preload_memory
- Zero-manual-intervention memory systems

Key Concept:
Callbacks trigger at specific lifecycle moments (before/after agent, tools, etc).
Use after_agent_callback to automatically save sessions to memory after each turn.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import preload_memory
from utils.model_config import get_text_model
from google.genai import types

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
    
    This callback is triggered after every agent response, ensuring
    all conversations are persistently stored in long-term memory.
    """
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


# Agent with automatic memory saving and loading
root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="auto_memory_agent",
    description="Agent with fully automated memory management",
    instruction="""You are a helpful assistant with automated long-term memory.
    
    Your conversations are automatically saved to memory after each turn.
    Memory is automatically loaded before each response, so you always have
    access to past conversations without needing to explicitly search.""",
    tools=[preload_memory],  # Proactive: always loads memory
    after_agent_callback=auto_save_to_memory,  # Automatic saving!
)
