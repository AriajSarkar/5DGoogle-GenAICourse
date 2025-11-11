"""
1b - Multi-Agent Systems: LLM-Based Coordinator Pattern (ADK App Structure)
============================================================================
This is the ADK-compatible version of 01_llm_coordinator_pattern.py

To run this with ADK CLI:
    adk run Day1/1b-agent-architectures/llm_coordinator

Concepts covered:
- Multi-agent systems vs. monolithic agents
- AgentTool wrapper for sub-agents
- LLM-based dynamic orchestration
- State management with output_key
"""

from utils.model_config import get_text_model

from google.adk.agents import Agent
from google.adk.tools import AgentTool, google_search

def create_research_agent():
    """Research Agent: Specialized for finding information using Google Search."""
    return Agent(
        name="ResearchAgent",
        model=get_text_model(),
        instruction="""You are a specialized research agent. Your only job is to use the
        google_search tool to find 2-3 pieces of relevant information on the given topic 
        and present the findings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

def create_summarizer_agent():
    """Summarizer Agent: Specialized for creating concise summaries."""
    return Agent(
        name="SummarizerAgent",
        model=get_text_model(),
        instruction="""Read the provided research findings: {research_findings}
        Create a concise summary as a bulleted list with 3-5 key points.""",
        output_key="final_summary",
    )

# Root agent: Coordinator that orchestrates sub-agents
root_agent = Agent(
    name="ResearchCoordinator",
    model=get_text_model(),
    instruction="""You are a research coordinator. Your goal is to answer the user's query 
    by orchestrating a workflow.
    1. First, you MUST call the `ResearchAgent` tool to find relevant information on the 
       topic provided by the user.
    2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` 
       tool to create a concise summary.
    3. Finally, present the final summary clearly to the user as your response.""",
    tools=[
        AgentTool(create_research_agent()),
        AgentTool(create_summarizer_agent())
    ],
)
