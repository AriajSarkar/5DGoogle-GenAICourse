"""
1b - Loop Agents: The Iterative Refinement Pattern (ADK App Structure)
=======================================================================
This is the ADK-compatible version of 04_loop_pattern.py

To run this with ADK CLI:
    adk run Day1/1b-agent-architectures/loop_pattern

Concepts covered:
- LoopAgent for iterative refinement
- FunctionTool for custom exit conditions
- Feedback and revision cycles
- Nested workflow (Sequential with Loop inside)
"""

from utils.model_config import get_text_model

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools import FunctionTool

def exit_loop():
    """
    Exit condition function for the loop.
    
    The RefinerAgent will call this function when the critique is "APPROVED",
    signaling the loop to terminate.
    """
    return {
        "status": "approved",
        "message": "Story approved. Exiting refinement loop."
    }

def create_initial_writer():
    """Initial Writer Agent: Creates the first draft."""
    return Agent(
        name="InitialWriterAgent",
        model=get_text_model(),
        instruction="""Based on the user's prompt, write the first draft of a short story 
        (around 100-150 words). Output only the story text, with no introduction or explanation.""",
        output_key="current_story",
    )

def create_critic_agent():
    """Critic Agent: Reviews and critiques the story."""
    return Agent(
        name="CriticAgent",
        model=get_text_model(),
        instruction="""You are a constructive story critic. Review the story provided below.
        Story: {current_story}
        
        Evaluate the story's plot, characters, and pacing.
        - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
        - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
        output_key="critique",
    )

def create_refiner_agent():
    """Refiner Agent: Improves the story OR exits the loop."""
    return Agent(
        name="RefinerAgent",
        model=get_text_model(),
        instruction="""You are a story refiner. You have a story draft and critique.
        
        Story Draft: {current_story}
        Critique: {critique}
        
        Your task is to analyze the critique.
        - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
        - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
        output_key="current_story",
        tools=[FunctionTool(exit_loop)],
    )

# Root agent: Nested workflow (Initial draft → Refinement loop)
# Architecture:
#   SequentialAgent
#     ├─ InitialWriterAgent (runs once)
#     └─ LoopAgent (repeats until approved or max iterations)
#          ├─ CriticAgent
#          └─ RefinerAgent

refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[create_critic_agent(), create_refiner_agent()],
    max_iterations=3,
)

root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[create_initial_writer(), refinement_loop],
)
