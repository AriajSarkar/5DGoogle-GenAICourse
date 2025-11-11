"""
1a - From Prompt to Action: Agent with Custom Tool (ADK App Structure)
=======================================================================
This is the ADK-compatible version of 02_agent_with_custom_tool.py

To run this with ADK CLI:
    adk run Day1/1a-from-prompt-to-action/02_agent_with_custom_tool

Concepts covered:
- Creating custom Python functions as tools
- Registering tools with root_agent
- Tool usage in ADK app structure
"""

from utils.model_config import get_text_model

from google.adk.agents import Agent
from datetime import datetime
import pytz

def get_current_time(city: str) -> dict:
    """
    Returns the current time in a specified city.
    
    Args:
        city: Name of the city (e.g., "London", "New York", "Tokyo")
    
    Returns:
        Dictionary with status, city, and current time
    """
    timezone_map = {
        "london": "Europe/London",
        "new york": "America/New_York",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
        "dubai": "Asia/Dubai",
        "singapore": "Asia/Singapore",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "toronto": "America/Toronto",
    }
    
    city_lower = city.lower()
    
    if city_lower in timezone_map:
        tz = pytz.timezone(timezone_map[city_lower])
        current_time = datetime.now(tz).strftime("%I:%M %p")
        return {
            "status": "success",
            "city": city,
            "time": current_time,
            "timezone": timezone_map[city_lower]
        }
    else:
        return {
            "status": "error",
            "city": city,
            "message": "City not found in database. Please try a major city."
        }

def get_weather_info(city: str) -> dict:
    """
    Mock function that returns weather information for a city.
    In a real scenario, this would call a weather API.
    
    Args:
        city: Name of the city
    
    Returns:
        Dictionary with mock weather data
    """
    return {
        "status": "success",
        "city": city,
        "temperature": "18°C",
        "condition": "Partly cloudy",
        "humidity": "65%",
        "note": "This is mock data for demonstration"
    }

# Root agent with custom tools
root_agent = Agent(
    name="time_weather_assistant",
    model=get_text_model(),
    description="An agent that can tell time and weather for cities.",
    instruction=(
        "You are a helpful assistant that provides time and weather information. "
        "Use the 'get_current_time' tool to get current time in cities. "
        "Use the 'get_weather_info' tool to get weather data. "
        "Always be friendly and clear in your responses."
    ),
    tools=[get_current_time, get_weather_info],
)
