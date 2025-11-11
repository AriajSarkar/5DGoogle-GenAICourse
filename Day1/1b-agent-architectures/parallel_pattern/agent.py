"""
1b - Parallel Agents: The Concurrent Execution Pattern (ADK App Structure)
===========================================================================
This is the ADK-compatible version of 03_parallel_pattern.py

To run this with ADK CLI:
    adk run Day1/1b-agent-architectures/03_parallel_pattern

Concepts covered:
- ParallelAgent for concurrent execution
- Speed optimization for independent tasks
- Aggregating parallel results
- Nested workflow patterns (Parallel inside Sequential)
"""

from utils.model_config import get_text_model

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

def create_tech_researcher():
    """Tech Researcher: Focuses on AI/ML trends."""
    return Agent(
        name="TechResearcher",
        model=get_text_model(),
        instruction="""Research the latest AI/ML trends. Include 3 key developments,
        the main companies involved, and the potential impact. Keep the report 
        very concise (100 words).""",
        tools=[google_search],
        output_key="tech_research",
    )

def create_health_researcher():
    """Health Researcher: Focuses on medical breakthroughs."""
    return Agent(
        name="HealthResearcher",
        model=get_text_model(),
        instruction="""Research recent medical breakthroughs. Include 3 significant advances,
        their practical applications, and estimated timelines. Keep the report 
        concise (100 words).""",
        tools=[google_search],
        output_key="health_research",
    )

def create_finance_researcher():
    """Finance Researcher: Focuses on fintech trends."""
    return Agent(
        name="FinanceResearcher",
        model=get_text_model(),
        instruction="""Research current fintech trends. Include 3 key trends,
        their market implications, and the future outlook. Keep the report 
        concise (100 words).""",
        tools=[google_search],
        output_key="finance_research",
    )

def create_aggregator_agent():
    """
    Aggregator Agent: Combines all research findings.
    
    Runs AFTER the parallel research agents complete.
    Uses {tech_research}, {health_research}, {finance_research} from state.
    """
    return Agent(
        name="AggregatorAgent",
        model=get_text_model(),
        instruction="""Combine these three research findings into a single executive summary:

        **Technology Trends:**
        {tech_research}
        
        **Health Breakthroughs:**
        {health_research}
        
        **Finance Innovations:**
        {finance_research}
        
        Your summary should highlight common themes, surprising connections, and the most 
        important key takeaways from all three reports. The final summary should be around 
        200 words.""",
        output_key="executive_summary",
    )

# Root agent: Nested workflow (Parallel → Sequential)
# Architecture:
#   SequentialAgent
#     ├─ ParallelAgent (runs all 3 researchers concurrently)
#     │    ├─ TechResearcher
#     │    ├─ HealthResearcher
#     │    └─ FinanceResearcher
#     └─ AggregatorAgent (runs after parallel completes)

parallel_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[
        create_tech_researcher(),
        create_health_researcher(),
        create_finance_researcher(),
    ],
)

root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_team, create_aggregator_agent()],
)
