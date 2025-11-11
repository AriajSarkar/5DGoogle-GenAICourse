"""
Shipping Approval Agent - Day 2b: Long-Running Operations
Based on Kaggle 5-Day Agents Course - Day 2b
Copyright 2025 Google LLC - Licensed under Apache 2.0

Demonstrates:
- Long-Running Operations (LRO) pattern
- Human-in-the-loop approvals
- Tool pause/resume workflow
- ToolContext and request_confirmation
- Resumable App configuration

This agent handles shipping orders with approval for large orders (>5 containers).
"""

from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.apps.app import App, ResumabilityConfig


# Configure retry options
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


LARGE_ORDER_THRESHOLD = 5


def place_shipping_order(
    num_containers: int, destination: str, tool_context: ToolContext
) -> dict:
    """Places a shipping order. Requires approval if ordering more than 5 containers.

    This demonstrates the long-running operation pattern:
    - Small orders: Auto-approve and complete immediately
    - Large orders: Pause for human approval, then resume

    Args:
        num_containers: Number of containers to ship
        destination: Shipping destination
        tool_context: ADK provides this automatically - enables pause/resume

    Returns:
        Dictionary with order status and details
    """

    # SCENARIO 1: Small orders (≤5 containers) auto-approve
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order auto-approved: {num_containers} containers to {destination}",
        }

    # SCENARIO 2: First call - Large order needs approval - PAUSE HERE
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large order: {num_containers} containers to {destination}. Approve?",
            payload={"num_containers": num_containers, "destination": destination},
        )
        return {
            "status": "pending",
            "message": f"Order for {num_containers} containers requires approval",
        }

    # SCENARIO 3: Resumed call - Handle approval response - RESUME HERE
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-HUMAN",
            "num_containers": num_containers,
            "destination": destination,
            "message": f"Order approved: {num_containers} containers to {destination}",
        }
    else:
        return {
            "status": "rejected",
            "message": f"Order rejected: {num_containers} containers to {destination}",
        }


# Create shipping agent with pausable tool
# For ADK CLI (adk run), expose the agent directly
# For programmatic use with workflow, wrap in App (see reference script)
root_agent = LlmAgent(
    name="shipping_agent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    instruction="""You are a shipping coordinator assistant.
    
    When users request to ship containers:
    1. Use the place_shipping_order tool with number of containers and destination
    2. If the order status is 'pending', inform user that approval is required
    3. After receiving the final result, provide a clear summary including:
       - Order status (approved/rejected)
       - Order ID (if available)
       - Number of containers and destination
    4. Keep responses concise but informative
    
    NOTE: In the ADK CLI, you cannot provide approval interactively.
    Try small orders (≤5 containers) which auto-approve immediately.
    For full approval workflow, see the reference script.
    """,
    tools=[FunctionTool(func=place_shipping_order)],
)


# For programmatic use with approval workflow:
# Wrap the agent in a resumable App to enable pause/resume
# See reference script for complete workflow implementation
#
# shipping_app = App(
#     name="shipping_coordinator",
#     root_agent=root_agent,
#     resumability_config=ResumabilityConfig(is_resumable=True),
# )
