"""
Research Paper Finder Agent - Intentionally Broken for Debugging Practice

This agent demonstrates observability debugging patterns using ADK web UI and DEBUG logs.
Contains a deliberate bug: count_papers expects List[str] but receives str.

Learning Objectives:
- Debug agent failures using adk web --log_level DEBUG
- Analyze function call traces in ADK web UI Events tab
- Inspect LLM request/response in DEBUG logs
- Practice symptom → logs → root cause → fix debugging pattern

Run with:
    adk web --log_level DEBUG Day4/4a-agent-observability/
    (Then select research_agent_debug from dropdown)
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from google.genai import types
from typing import List
from utils.model_config import get_text_model

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
root_agent = LlmAgent(
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
