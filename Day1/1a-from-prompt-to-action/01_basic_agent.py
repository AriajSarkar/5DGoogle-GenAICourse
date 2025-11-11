"""
1a - From Prompt to Action: Basic Agent
========================================
This script demonstrates creating a simple AI agent with ADK.

Concepts covered:
- Creating an Agent instance
- Setting up InMemoryRunner
- Running an agent with run_debug()
"""

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
import asyncio


def create_basic_agent():
    """
    Create a basic agent without any tools.
    This agent can only use its base LLM capabilities.
    """
    agent = Agent(
        name="basic_assistant",
        model="gemini-2.5-flash",
        description="A simple agent that answers questions using only LLM knowledge.",
        instruction="You are a helpful assistant. Answer questions clearly and concisely.",
    )
    return agent


async def run_basic_agent():
    """Run the basic agent with a simple question."""
    print("=" * 60)
    print("Basic Agent Demo")
    print("=" * 60)
    
    # Create the agent
    agent = create_basic_agent()
    
    # Create a runner
    runner = InMemoryRunner(agent=agent)
    
    # Ask a simple question
    question = "What is artificial intelligence?"
    print(f"\nQuestion: {question}\n")
    
    response = await runner.run_debug(question)
    print(f"\nResponse received!\n")
    
    return response


if __name__ == "__main__":
    # Run the async function
    asyncio.run(run_basic_agent())
