"""
Day 3a Example 4: Session State Management

Demonstrates:
- Creating tools that read/write session state
- Sharing structured data across conversation turns
- Understanding state scope levels (user:, app:, temp:)

Key Concept:
Session state is a key-value store accessible to all tools. Use it to share
data across turns without re-asking the user (e.g., preferences, context).
"""

from typing import Dict, Any
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.tool_context import ToolContext
from utils.model_config import get_text_model
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Tool to save user info to session state
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
    # Write to session state using 'user:' prefix for user-specific data
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country
    
    return {"status": "success", "message": f"Saved {user_name} from {country}"}


# Tool to retrieve user info from session state
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


# Agent with session state tools
root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="state_demo_agent",
    description="Agent demonstrating session state management",
    instruction="""You are a helpful assistant.
    
    Tools for managing user context:
    - Use `save_userinfo` when the user provides their name and country
    - Use `retrieve_userinfo` when you need to recall the user's name or country
    
    When the user introduces themselves, save their information immediately.
    When asked about their details, retrieve from session state.""",
    tools=[save_userinfo, retrieve_userinfo],
)
