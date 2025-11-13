"""
Home Automation Agent - Regression Testing Demo

This agent demonstrates automated regression testing using adk eval CLI.
Shows how to detect performance degradation over time with batch testing.

Learning Objectives:
- Create evaluation configuration (test_config.json)
- Create test cases programmatically (*.evalset.json)
- Run CLI evaluation: adk eval agent/ evalset.json --config_file_path
- Analyze detailed results with --print_detailed_results

Run with:
    adk eval regression_testing/ regression_testing/integration.evalset.json --config_file_path=regression_testing/test_config.json --print_detailed_results
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from utils.model_config import get_text_model

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


def set_device_status(location: str, device_id: str, status: str) -> dict:
    """
    Sets the status of a smart home device.
    
    Args:
        location: The room where the device is located.
        device_id: The unique identifier for the device.
        status: The desired status, either 'ON' or 'OFF'.
    
    Returns:
        A dictionary confirming the action.
    """
    return {
        "success": True,
        "message": f"Successfully set the {device_id} in {location} to {status.lower()}."
    }


root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="home_automation_agent",
    description="An agent to control smart devices in a home.",
    instruction="""You are a home automation assistant. You control smart devices.
    
    When the user asks to control a device, use the set_device_status tool with the exact location,
    device_id, and status (ON or OFF) specified by the user.
    
    Respond with a confirmation message.""",
    tools=[set_device_status],
)
