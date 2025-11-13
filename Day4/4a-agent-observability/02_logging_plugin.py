"""
Day 4a: Agent Observability - Production Logging with LoggingPlugin

This script demonstrates production observability using ADK's built-in LoggingPlugin.
Shows how to capture comprehensive agent activity for production systems.

Learning Objectives:
- Use LoggingPlugin for automatic observability
- Understand plugin registration with InMemoryRunner
- Capture all agent events: user messages, tool calls, LLM requests
- Scale observability beyond development debugging

Key Concepts:
1. LoggingPlugin: Built-in plugin for comprehensive logging
2. Plugin Registration: Add to runner.plugins=[LoggingPlugin()]
3. Event Logging: Automatic capture of all agent lifecycle events
4. Production Ready: No code changes needed, just plugin registration

Run this script:
    python Day4/4a-agent-observability/02_logging_plugin.py
"""

import asyncio
import logging
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai import types
from typing import List
from utils.model_config import get_text_model

# Configure logging for LoggingPlugin output
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


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
    print("📊 Day 4a: Production Observability with LoggingPlugin")
    print("=" * 60)
    print()
    print("📋 Scenario: Research Paper Finder Agent (FIXED)")
    print("🎯 Goal: Find and count quantum computing papers")
    print("🔧 Observability: LoggingPlugin for production logging")
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
    
    # Root agent (fixed)
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
    
    # Register LoggingPlugin for automatic observability
    runner = InMemoryRunner(
        agent=research_agent,
        plugins=[LoggingPlugin()]  # <-- Automatic comprehensive logging
    )
    
    print("🚀 Running agent with LoggingPlugin...")
    print("📊 Watch the comprehensive logging output below:")
    print()
    
    response = await runner.run_debug("Find recent papers on quantum computing")
    
    print()
    print("=" * 60)
    print("📊 LOGGING ANALYSIS")
    print("=" * 60)
    print()
    print("✅ LoggingPlugin Captured:")
    print("   🚀 USER MESSAGE RECEIVED - Initial query")
    print("   🏃 INVOCATION STARTING - Agent execution begins")
    print("   🤖 AGENT STARTING - research_paper_finder_agent")
    print("   🧠 LLM REQUEST - Model call with system instruction")
    print("   🧠 LLM RESPONSE - Model decides to call google_search_agent")
    print("   🔧 TOOL STARTING - google_search_agent invocation")
    print("   🔧 TOOL COMPLETED - Search results returned")
    print("   🧠 LLM REQUEST - Second model call")
    print("   🧠 LLM RESPONSE - Model decides to call count_papers")
    print("   🔧 TOOL STARTING - count_papers invocation")
    print("   🔧 TOOL COMPLETED - Count returned")
    print("   🧠 LLM REQUEST - Final model call")
    print("   🧠 LLM RESPONSE - Final response generated")
    print("   ✅ INVOCATION COMPLETED")
    print()
    print("🎯 Key Benefits:")
    print("   • No manual logging code needed")
    print("   • Captures ALL agent lifecycle events")
    print("   • Production-ready observability")
    print("   • Easy integration: just add plugin to runner")
    print()
    print("📚 When to Use:")
    print("   Development debugging? → adk web --log_level DEBUG")
    print("   Production observability? → LoggingPlugin()")
    print("   Custom requirements? → Build custom callbacks/plugins")


if __name__ == "__main__":
    asyncio.run(main())
