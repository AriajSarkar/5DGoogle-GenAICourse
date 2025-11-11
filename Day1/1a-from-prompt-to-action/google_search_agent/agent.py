"""
1a - From Prompt to Action: Agent with Google Search (ADK App Structure)
=========================================================================
This is the ADK-compatible version of 03_agent_with_google_search.py

To run this with ADK CLI:
    adk run Day1/1a-from-prompt-to-action/google_search_agent

Concepts covered:
- Using ADK's built-in tools
- Google Search integration
- Handling real-time information queries
- Environment-based model configuration
"""

from utils.model_config import get_text_model
from google.adk.agents import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

# Root agent with Google Search capability
root_agent = Agent(
    name="search_assistant",
    model=get_text_model(),  # From env: GEMINI_TEXT_MODEL or default
    description="An agent that can search Google for current information.",
    instruction=(
        "You are a helpful assistant with access to Google Search. "
        "Use Google Search when you need current information, recent events, "
        "or facts you're not certain about. "
        "Always cite your sources when providing information from search results."
    ),
    tools=[GoogleSearchTool()],
)
