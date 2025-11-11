"""
1a - From Prompt to Action: Multi-Tool Agent (ADK App Structure)
=================================================================
This is the ADK-compatible version of 04_multi_tool_agent.py

To run this with ADK CLI:
    adk run Day1/1a-from-prompt-to-action/multi_tool_agent

Concepts covered:
- Combining custom tools with built-in tools
- Agent decision-making for tool selection
- Complex task handling
"""

from utils.model_config import get_text_model

from google.adk.agents import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from datetime import datetime
import pytz

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    timezone_map = {
        "london": "Europe/London",
        "new york": "America/New_York",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
    }
    
    city_lower = city.lower()
    if city_lower in timezone_map:
        tz = pytz.timezone(timezone_map[city_lower])
        current_time = datetime.now(tz).strftime("%I:%M %p, %B %d, %Y")
        return {
            "status": "success",
            "city": city,
            "time": current_time,
        }
    else:
        return {
            "status": "error",
            "city": city,
            "message": "City not found"
        }

def calculate_time_difference(city1: str, city2: str) -> dict:
    """
    Calculate the time difference between two cities.
    
    Args:
        city1: First city name
        city2: Second city name
    
    Returns:
        Dictionary with time difference information
    """
    timezone_map = {
        "london": "Europe/London",
        "new york": "America/New_York",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
    }
    
    city1_lower = city1.lower()
    city2_lower = city2.lower()
    
    if city1_lower in timezone_map and city2_lower in timezone_map:
        tz1 = pytz.timezone(timezone_map[city1_lower])
        tz2 = pytz.timezone(timezone_map[city2_lower])
        
        now = datetime.now(pytz.UTC)
        time1 = now.astimezone(tz1)
        time2 = now.astimezone(tz2)
        
        # Calculate offset difference in hours
        offset_diff = (time1.utcoffset().total_seconds() - time2.utcoffset().total_seconds()) / 3600
        
        return {
            "status": "success",
            "city1": city1,
            "city2": city2,
            "time_difference_hours": offset_diff,
            "description": f"{city1} is {abs(offset_diff)} hours {'ahead of' if offset_diff > 0 else 'behind'} {city2}"
        }
    else:
        return {
            "status": "error",
            "message": "One or both cities not found"
        }

# Root agent with multiple tools (custom + built-in)
root_agent = Agent(
    name="multi_tool_assistant",
    model=get_text_model(),
    description="A versatile agent with time, calculation, and search capabilities.",
    instruction=(
        "You are a helpful assistant with multiple capabilities:\n"
        "1. Use 'get_current_time' to tell time in specific cities\n"
        "2. Use 'calculate_time_difference' to compare times between cities\n"
        "3. Use GoogleSearchTool to find current information, news, or facts\n\n"
        "Choose the appropriate tool based on the user's question. "
        "You can use multiple tools in sequence if needed."
    ),
    tools=[
        get_current_time,
        calculate_time_difference,
        GoogleSearchTool(),
    ],
)
