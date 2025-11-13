"""
Day 4a: Agent Observability - Debugging with DEBUG Logs

This script demonstrates how to debug agent failures using DEBUG log levels.
Contains an intentionally broken agent to practice debugging workflows.

Learning Objectives:
- Configure logging with DEBUG level
- Identify bugs from LLM request/response logs
- Understand the debugging pattern: symptom → logs → root cause → fix
- Use adk web --log_level DEBUG for interactive debugging

Key Concepts:
1. DEBUG Logging: Captures full LLM prompts, tool calls, and responses
2. Root Cause Analysis: Inspect function_call parts to find parameter mismatches
3. Fix Verification: Re-run with corrected code to validate fix

Run this script:
    python Day4/4a-agent-observability/01_debug_with_logs.py

For interactive debugging:
    adk web --log_level DEBUG Day4/4a-agent-observability/
"""

import asyncio
import logging
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from google.genai import types
from typing import List
from utils.model_config import get_text_model

# Configure DEBUG logging to capture detailed agent execution
logging.basicConfig(
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
)

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


# INTENTIONALLY BROKEN: Type hint says str but should be List[str]
def count_papers(papers: str):
    """
    Counts the number of research papers in a list.
    
    Args:
        papers: A list of strings, where each string is a research paper.
    
    Returns:
        The number of papers in the list.
    """
    return len(papers)


async def main():
    print("🐞 Day 4a: Debugging Agent with DEBUG Logs")
    print("=" * 60)
    print()
    print("📋 Scenario: Research Paper Finder Agent (BROKEN)")
    print("🎯 Goal: Find and count quantum computing papers")
    print("🔍 Debugging Tool: DEBUG logs showing LLM requests/responses")
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
    
    # Root agent with broken tool
    research_agent = LlmAgent(
        name="research_paper_finder_agent",
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        instruction="""Your task is to find research papers and count them.
        
        You MUST ALWAYS follow these steps:
        1) Find research papers on the user provided topic using the 'google_search_agent'.
        2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
        3) Return both the list of research papers and the total number of papers.
        """,
        tools=[AgentTool(agent=google_search_agent), count_papers]
    )
    
    runner = InMemoryRunner(agent=research_agent)
    
    print("🚀 Running broken agent...")
    print("👀 Watch DEBUG logs for clues!")
    print()
    
    response = await runner.run_debug("Find latest quantum computing papers")
    
    print()
    print("=" * 60)
    print("📊 DEBUGGING ANALYSIS")
    print("=" * 60)
    print()
    print("🔍 What happened:")
    print("   • Agent found papers via google_search_agent")
    print("   • Agent called count_papers tool")
    print("   • COUNT IS UNUSUALLY LARGE (e.g., 5000+)")
    print()
    print("🕵️ Root Cause (from DEBUG logs):")
    print("   1. Search DEBUG logs for 'function_call: count_papers'")
    print("   2. Check the 'papers' argument in LLM Request")
    print("   3. Notice: papers passed as STRING instead of LIST")
    print("   4. Bug: count_papers(papers: str) counts characters, not list items")
    print()
    print("💡 The Fix:")
    print("   Change: def count_papers(papers: str)")
    print("   To:     def count_papers(papers: List[str])")
    print()
    print("✅ Debugging Pattern:")
    print("   Symptom → DEBUG logs → Root cause → Fix → Verify")
    print()
    print("🎯 Try It:")
    print("   1. Examine DEBUG logs above for 'LLM Request' and 'LLM Response'")
    print("   2. Find the function_call for count_papers")
    print("   3. Confirm papers argument is a string (containing all text)")
    print("   4. Update count_papers to use List[str] type hint")


if __name__ == "__main__":
    asyncio.run(main())
