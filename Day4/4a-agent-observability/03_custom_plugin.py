"""
Day 4a: Agent Observability - Custom Plugin for Metrics Tracking

This script demonstrates custom plugin creation for specialized observability.
Shows how to build plugins with callbacks to track custom metrics.

Learning Objectives:
- Create custom plugins by extending BasePlugin
- Implement before_agent_callback and before_model_callback
- Track custom metrics (agent invocations, LLM requests, tool calls)
- Understand when to use custom plugins vs LoggingPlugin

Key Concepts:
1. Custom Plugins: Extend BasePlugin for specialized needs
2. Callbacks: Hook into agent lifecycle (before/after agent, model, tool)
3. Metrics Tracking: Count invocations, measure latency, etc.
4. Plugin Registration: Add to runner.plugins like LoggingPlugin

Run this script:
    python Day4/4a-agent-observability/03_custom_plugin.py
"""

import asyncio
import logging
from google.adk.agents import LlmAgent
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from google.adk.models.llm_request import LlmRequest
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from google.adk.plugins.base_plugin import BasePlugin
from google.genai import types
from typing import List
from utils.model_config import get_text_model

logging.basicConfig(level=logging.INFO, format="%(message)s")

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# Custom Plugin for tracking invocation counts
class CountInvocationPlugin(BasePlugin):
    """A custom plugin that counts agent and LLM invocations."""
    
    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="count_invocation")
        self.agent_count: int = 0
        self.llm_request_count: int = 0
    
    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent runs."""
        self.agent_count += 1
        logging.info(f"[CountPlugin] 🤖 Agent run #{self.agent_count}: {agent.name}")
    
    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.llm_request_count += 1
        logging.info(f"[CountPlugin] 🧠 LLM request #{self.llm_request_count}")


def count_papers(papers: List[str]):
    """
    Counts the number of research papers in a list.
    
    Args:
        papers: A list of strings, where each string is a research paper.
    
    Returns:
        The number of papers in the list.
    """
    return len(papers)


async def main():
    print("🔧 Day 4a: Custom Plugin for Metrics Tracking")
    print("=" * 60)
    print()
    print("📋 Scenario: Research Paper Finder with Custom Metrics")
    print("🎯 Goal: Track agent and LLM invocation counts")
    print("🔧 Observability: CountInvocationPlugin")
    print()
    
    # Google Search agent
    google_search_agent = LlmAgent(
        name="google_search_agent",
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        description="Searches for information using Google search",
        instruction="""Use the google_search tool to find information on the given topic. Return the raw search results.
        If the user asks for a list of papers, give them the list of research papers you found, not a summary.""",
        tools=[google_search]
    )
    
    # Root agent
    research_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        instruction="""Your task is to find research papers and count them.
        
        You must follow these steps:
        1) Find research papers on the user provided topic using the 'google_search_agent'.
        2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
        3) Return both the list of research papers and the total number of papers.
        """,
        tools=[AgentTool(agent=google_search_agent), count_papers]
    )
    
    # Register custom plugin
    custom_plugin = CountInvocationPlugin()
    runner = InMemoryRunner(
        agent=research_agent,
        plugins=[custom_plugin]  # <-- Custom plugin for metrics
    )
    
    print("🚀 Running agent with CountInvocationPlugin...")
    print("📊 Watch custom metrics below:")
    print()
    
    response = await runner.run_debug("Find recent papers on quantum computing")
    
    print()
    print("=" * 60)
    print("📊 CUSTOM METRICS SUMMARY")
    print("=" * 60)
    print()
    print(f"🤖 Total Agent Invocations: {custom_plugin.agent_count}")
    print(f"🧠 Total LLM Requests: {custom_plugin.llm_request_count}")
    print()
    print("🔍 Breakdown:")
    print("   • research_paper_finder_agent: 1 invocation")
    print("   • google_search_agent: 1 invocation (via AgentTool)")
    print("   • LLM calls: ~3-4 (depends on tool call flow)")
    print()
    print("=" * 60)
    print("🎓 CUSTOM PLUGIN PATTERNS")
    print("=" * 60)
    print()
    print("✅ When to Build Custom Plugins:")
    print("   • Track business-specific metrics (cost, latency)")
    print("   • Implement security checks (input validation)")
    print("   • Add caching layers (reduce LLM calls)")
    print("   • Integrate with external monitoring (DataDog, Prometheus)")
    print()
    print("🔧 Available Callbacks:")
    print("   • before/after_agent_callback - Agent lifecycle")
    print("   • before/after_tool_callback - Tool execution")
    print("   • before/after_model_callback - LLM requests")
    print("   • on_model_error_callback - Error handling")
    print()
    print("📚 Plugin Architecture:")
    print("   Runner → Plugin → Callbacks → Custom Logic")
    print("   (Applies automatically to ALL agents and tools)")


if __name__ == "__main__":
    asyncio.run(main())
