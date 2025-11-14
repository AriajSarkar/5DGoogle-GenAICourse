"""
Weather Agent (Production-Ready for Deployment)

This agent demonstrates a production-ready ADK agent optimized for deployment.

KEY CONCEPTS:
- Production model selection: gemini-2.5-flash-lite for cost/latency
- Clean tool design: Simple, focused function with clear docstring
- Structured responses: Consistent return format for reliability
- Deployment-ready: Minimal dependencies, fast execution

DEPLOYMENT OPTIONS:
This agent can be deployed to:
1. Vertex AI Agent Engine: adk deploy agent_engine weather_agent_deploy/
2. Cloud Run: adk deploy cloud_run weather_agent_deploy/
3. GKE: adk deploy gke weather_agent_deploy/

RUN LOCALLY:
    adk run Day5/5b-agent-deployment/weather_agent_deploy/
    
DEPLOY TO AGENT ENGINE:
    # Set your project ID
    $env:GOOGLE_CLOUD_PROJECT="your-project-id"
    
    # Deploy (requires GCP account and billing)
    adk deploy agent_engine Day5/5b-agent-deployment/weather_agent_deploy/ `
        --project=$env:GOOGLE_CLOUD_PROJECT `
        --region=us-west1

CONFIGURATION FILES NEEDED:
- .env: GOOGLE_CLOUD_LOCATION, GOOGLE_GENAI_USE_VERTEXAI
- requirements.txt: Dependencies for deployment
- .agent_engine_config.json: Resource limits (CPU, memory, instances)

See 01_deploy_to_agent_engine.py for complete deployment example.
"""

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from utils.model_config import get_text_model


def get_weather(city: str) -> dict:
    """
    Returns weather information for a given city.
    
    This is a TOOL that the agent can call when users ask about weather.
    In production, this would call a real weather API (e.g., OpenWeatherMap).
    For this demo, we use mock data.
    
    Args:
        city: Name of the city (e.g., "Tokyo", "New York")
    
    Returns:
        dict: Dictionary with status and weather report or error message
    """
    # Mock weather database with structured responses
    weather_data = {
        "san francisco": {
            "status": "success",
            "city": "San Francisco",
            "temperature": "72°F (22°C)",
            "conditions": "Sunny",
            "humidity": "65%",
            "wind": "10 mph"
        },
        "new york": {
            "status": "success",
            "city": "New York",
            "temperature": "65°F (18°C)",
            "conditions": "Cloudy",
            "humidity": "70%",
            "wind": "12 mph"
        },
        "london": {
            "status": "success",
            "city": "London",
            "temperature": "58°F (14°C)",
            "conditions": "Rainy",
            "humidity": "85%",
            "wind": "15 mph"
        },
        "tokyo": {
            "status": "success",
            "city": "Tokyo",
            "temperature": "70°F (21°C)",
            "conditions": "Clear",
            "humidity": "60%",
            "wind": "8 mph"
        },
        "paris": {
            "status": "success",
            "city": "Paris",
            "temperature": "68°F (20°C)",
            "conditions": "Partly Cloudy",
            "humidity": "68%",
            "wind": "11 mph"
        }
    }
    
    city_lower = city.lower()
    
    if city_lower in weather_data:
        return weather_data[city_lower]
    else:
        available_cities = ", ".join([c.title() for c in weather_data.keys()])
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available. Try: {available_cities}"
        }


# Create production-ready Weather Agent
# Uses Agent (not LlmAgent) for simplicity - Agent Engine will configure LLM backend
root_agent = Agent(
    name="weather_assistant",
    model=get_text_model(),  # Environment-based model selection
    description="A helpful weather assistant that provides weather information for cities.",
    instruction="""
    You are a friendly weather assistant. When users ask about the weather:
    
    1. Identify the city name from their question
    2. Use the get_weather tool to fetch current weather information
    3. Respond in a friendly, conversational tone
    4. If the city isn't available, suggest one of the available cities
    
    Be helpful and concise in your responses.
    """,
    tools=[get_weather]
)
