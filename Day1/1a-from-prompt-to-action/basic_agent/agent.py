"""
1a - From Prompt to Action: Basic Agent (ADK App Structure)
============================================================
This is the ADK-compatible version of 01_basic_agent.py

To run this with ADK CLI:
    adk run Day1/1a-from-prompt-to-action/basic_agent

Concepts covered:
- Creating an Agent for use with adk run
- Proper root_agent structure
- ADK app folder organization
- Environment-based model configuration

Based on Kaggle 5-Day Agents Course - Day 1a
Copyright 2025 Google LLC - Licensed under Apache 2.0
"""

from utils.model_config import get_text_model
from google.adk.agents import Agent

# This is the root agent that adk run expects
# Uses environment-based model configuration (default: gemini-2.5-flash-lite)
root_agent = Agent(
    name="basic_assistant",
    model=get_text_model(),  # From env: GEMINI_TEXT_MODEL or default
    description="A simple agent that answers questions using only LLM knowledge.",
    instruction="You are a helpful assistant. Answer questions clearly and concisely.",
)
