"""
Memory-Enabled Weather Agent (Production Deployment)

This agent demonstrates Memory Bank integration for long-term memory across sessions.

KEY CONCEPTS:
- PreloadMemoryTool: Automatically loads relevant memories before each turn
- After-agent callback: Saves conversations to Memory Bank
- Cross-session recall: Agent remembers user preferences across days/weeks
- Vertex AI Memory Bank: LLM-powered memory consolidation + semantic search

MEMORY BANK vs SESSION MEMORY:
- Session Memory: Single conversation (forgets when session ends)
- Memory Bank: All conversations (remembers permanently)

EXAMPLE USE CASE:
Session 1: User: "I prefer Celsius"
Session 2 (days later): User: "Weather in Tokyo?" 
→ Agent responds in Celsius automatically ✨

DEPLOYMENT:
This agent requires Memory Bank to be enabled in your GCP project:
1. Enable Memory Bank in Vertex AI Console
2. Deploy agent with memory configuration
3. Agent automatically uses Memory Bank

RUN LOCALLY (with InMemoryMemoryService):
    adk run Day5/5b-agent-deployment/memory_enabled_agent/
    
DEPLOY TO AGENT ENGINE (with Vertex AI Memory Bank):
    adk deploy agent_engine Day5/5b-agent-deployment/memory_enabled_agent/ `
        --project=your-project-id `
        --region=us-west1
    
    # Memory Bank is automatically configured when deployed to Agent Engine

MEMORY WORKFLOW:
1. User asks question
2. PreloadMemoryTool searches Memory Bank for relevant facts
3. Agent uses retrieved memories in response
4. After-agent callback saves conversation to Memory Bank
5. Next session: Agent recalls and uses saved information

See 02_memory_bank_integration.py for local testing with InMemoryMemoryService.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import preload_memory
from utils.model_config import get_text_model


def get_weather(city: str) -> dict:
    """
    Returns weather information for a given city.
    
    Args:
        city: Name of the city (e.g., "Tokyo", "New York")
    
    Returns:
        dict: Dictionary with status and weather report
    """
    weather_data = {
        "san francisco": {
            "status": "success",
            "city": "San Francisco",
            "temperature_f": 72,
            "temperature_c": 22,
            "conditions": "Sunny"
        },
        "new york": {
            "status": "success",
            "city": "New York",
            "temperature_f": 65,
            "temperature_c": 18,
            "conditions": "Cloudy"
        },
        "tokyo": {
            "status": "success",
            "city": "Tokyo",
            "temperature_f": 70,
            "temperature_c": 21,
            "conditions": "Clear"
        },
        "paris": {
            "status": "success",
            "city": "Paris",
            "temperature_f": 68,
            "temperature_c": 20,
            "conditions": "Partly Cloudy"
        }
    }
    
    city_lower = city.lower()
    
    if city_lower in weather_data:
        return weather_data[city_lower]
    else:
        available = ", ".join([c.title() for c in weather_data.keys()])
        return {
            "status": "error",
            "error_message": f"Weather info for '{city}' not available. Try: {available}"
        }


# Callback to automatically save conversations to Memory Bank
async def auto_save_to_memory(callback_context):
    """
    After-agent callback that saves each conversation turn to Memory Bank.
    
    This enables cross-session recall:
    - User preferences are remembered
    - Agent can reference past conversations
    - Memory persists across days/weeks
    
    When deployed to Agent Engine, this uses Vertex AI Memory Bank.
    When testing locally, use InMemoryMemoryService (see 02_memory_bank_integration.py).
    """
    # Access memory service from invocation context
    memory_service = callback_context._invocation_context.memory_service
    
    if memory_service:
        # Save current session to memory
        session = callback_context._invocation_context.session
        await memory_service.add_session_to_memory(session)


# Create Memory-Enabled Weather Agent
root_agent = LlmAgent(
    model=Gemini(model=get_text_model()),
    name="weather_assistant_with_memory",
    description="A weather assistant with long-term memory that remembers user preferences.",
    instruction="""
    You are a friendly weather assistant with long-term memory.
    
    MEMORY CAPABILITIES:
    - Remember user preferences (temperature unit, favorite cities)
    - Recall past conversations
    - Use memories to personalize responses
    
    When users ask about weather:
    1. Use preload_memory tool to check for user preferences (Celsius/Fahrenheit)
    2. Use get_weather tool to fetch current weather
    3. Format response according to user's preferred temperature unit
    4. Be friendly and personalize based on remembered information
    
    PREFERENCE HANDLING:
    - If user says "I prefer Celsius", remember for future queries
    - If user says "I prefer Fahrenheit", remember for future queries
    - If no preference stored, provide both units
    
    Example:
    - Memory: User prefers Celsius
    - Query: "What's the weather in Tokyo?"
    - Response: "Tokyo is clear with a temperature of 21°C."
    """,
    tools=[
        get_weather,
        preload_memory,  # Automatically loads relevant memories before each turn
    ],
    after_agent_callback=auto_save_to_memory,  # Automatically saves after each turn
)
