"""
Enhanced Currency Converter Agent - Day 2a: Agent Tools with Code Execution
Based on Kaggle 5-Day Agents Course - Day 2a
Copyright 2025 Google LLC - Licensed under Apache 2.0

Demonstrates:
- Custom Function Tools
- Agent as Tool (AgentTool wrapper)
- Built-in Code Executor for reliable calculations
- Multi-agent coordination (currency agent + calculation agent)
"""

from utils.model_config import get_text_model

from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

# Configure retry options
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

def get_fee_for_payment_method(method: str) -> dict:
    """Looks up the transaction fee percentage for a given payment method.

    Args:
        method: The name of the payment method (e.g., "platinum credit card").

    Returns:
        Dictionary with status and fee information.
    """
    fee_database = {
        "platinum credit card": 0.02,
        "gold debit card": 0.035,
        "bank transfer": 0.01,
    }

    fee = fee_database.get(method.lower())
    if fee is not None:
        return {"status": "success", "fee_percentage": fee}
    else:
        return {
            "status": "error",
            "error_message": f"Payment method '{method}' not found",
        }

def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Looks up and returns the exchange rate between two currencies.

    Args:
        base_currency: ISO 4217 code (e.g., "USD").
        target_currency: ISO 4217 code (e.g., "EUR").

    Returns:
        Dictionary with status and rate information.
    """
    rate_database = {
        "usd": {
            "eur": 0.93,
            "jpy": 157.50,
            "inr": 83.58,
        }
    }

    base = base_currency.lower()
    target = target_currency.lower()

    rate = rate_database.get(base, {}).get(target)
    if rate is not None:
        return {"status": "success", "rate": rate}
    else:
        return {
            "status": "error",
            "error_message": f"Unsupported currency pair: {base_currency}/{target_currency}",
        }

# Calculation agent - generates Python code for precise math
calculation_agent = LlmAgent(
    name="CalculationAgent",
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    instruction="""You are a specialized calculator that ONLY responds with Python code.
    
    **RULES:**
    1. Your output MUST be ONLY a Python code block.
    2. Do NOT write any text before or after the code block.
    3. The Python code MUST calculate the result.
    4. The Python code MUST print the final result to stdout.
    5. You are PROHIBITED from performing the calculation yourself.
    
    Failure to follow these rules will result in an error.
    """,
    code_executor=BuiltInCodeExecutor(),
)

# Enhanced currency agent that delegates calculations
root_agent = LlmAgent(
    name="enhanced_currency_agent",
    model=Gemini(model=get_text_model(), retry_options=retry_config),
    instruction="""You are a smart currency conversion assistant. You must strictly follow these steps.

    For any currency conversion request:

    1. Get Transaction Fee: Use get_fee_for_payment_method() to determine the fee.
    2. Get Exchange Rate: Use get_exchange_rate() to get the conversion rate.
    3. Error Check: After each tool call, check the "status" field. If "error", stop and explain.
    4. Calculate Final Amount (CRITICAL): You are strictly prohibited from performing arithmetic 
       calculations yourself. You must use the calculation_agent tool to generate Python code 
       that calculates the final converted amount using the fee and exchange rate.
    5. Provide Detailed Breakdown: In your summary, you must:
       * State the final converted amount.
       * Explain the calculation including:
         - Fee percentage and amount in original currency
         - Amount remaining after deducting the fee
         - Exchange rate applied
    """,
    tools=[
        get_fee_for_payment_method,
        get_exchange_rate,
        AgentTool(agent=calculation_agent),  # Using another agent as a tool!
    ],
)
