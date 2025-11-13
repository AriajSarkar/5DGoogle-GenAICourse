"""
Home Automation Agent - Evaluation Demo

This agent demonstrates evaluation workflow using ADK web UI and CLI.
Intentionally overconfident to reveal issues through comprehensive testing.

Learning Objectives:
- Create test cases interactively in ADK web UI
- Run evaluations with response_match and tool_trajectory metrics
- Analyze pass/fail results in Evaluation History
- Understand evaluation as proactive quality assurance

Run with:
    adk web Day4/4b-agent-evaluation/
    (Then select home_automation_eval from dropdown)
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


# Agent with DELIBERATE FLAWS for evaluation practice
root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="home_automation_agent",
    description="An agent to control smart devices in a home.",
    instruction="""You are a home automation assistant. You control ALL smart devices in the house.
    
    You have access to lights, security systems, ovens, fireplaces, and any other device the user mentions.
    Always try to be helpful and control whatever device the user asks for.
    
    When users ask about device capabilities, tell them about all the amazing features you can control.""",
    tools=[set_device_status],
)
