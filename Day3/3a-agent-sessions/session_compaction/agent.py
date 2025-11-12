"""
Day 3a Example 3: Context Compaction for Long Conversations

Demonstrates:
- Automatic history summarization with EventsCompactionConfig
- Managing token costs in long conversations
- Balancing context retention vs efficiency

Key Concept:
Long conversations consume massive tokens (Turn 1: 100, Turn 2: 200, Turn 3: 300...).
Context compaction automatically summarizes old turns, keeping recent context.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from utils.model_config import get_text_model
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Agent for demonstrating context compaction
root_agent = LlmAgent(
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    name="compaction_demo_agent",
    description="Agent demonstrating automatic context compaction",
    instruction="""You are a research assistant. Answer questions about AI topics.
    You will be used to demonstrate context compaction in long conversations.""",
)
