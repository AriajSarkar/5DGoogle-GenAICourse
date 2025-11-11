"""
1b - Sequential Agents: The Assembly Line Pattern
==================================================
This script demonstrates the Sequential Agent pattern for deterministic,
ordered execution of sub-agents.

Concepts covered:
- SequentialAgent for guaranteed execution order
- Pipeline workflows (Outline → Write → Edit)
- State passing between agents with output_key
- Fixed, predictable workflows
"""

from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner
import asyncio


def create_outline_agent():
    """
    Outline Agent: Creates a structured blog post outline.
    """
    return Agent(
        name="OutlineAgent",
        model="gemini-2.5-flash",
        instruction="""Create a blog outline for the given topic with:
        1. A catchy headline
        2. An introduction hook
        3. 3-5 main sections with 2-3 bullet points for each
        4. A concluding thought""",
        output_key="blog_outline",
    )


def create_writer_agent():
    """
    Writer Agent: Writes a full blog post based on the outline.
    
    Note: {blog_outline} is automatically injected from the previous agent's output.
    """
    return Agent(
        name="WriterAgent",
        model="gemini-2.5-flash",
        instruction="""Following this outline strictly: {blog_outline}
        Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
        output_key="blog_draft",
    )


def create_editor_agent():
    """
    Editor Agent: Polishes and refines the draft.
    
    Note: {blog_draft} is automatically injected from the writer agent's output.
    """
    return Agent(
        name="EditorAgent",
        model="gemini-2.5-flash",
        instruction="""Edit this draft: {blog_draft}
        Your task is to polish the text by fixing any grammatical errors, improving 
        the flow and sentence structure, and enhancing overall clarity.""",
        output_key="final_blog",
    )


def create_blog_pipeline():
    """
    Create a Sequential Agent that runs the blog creation pipeline.
    
    The agents run in the exact order listed: Outline → Write → Edit
    """
    outline_agent = create_outline_agent()
    writer_agent = create_writer_agent()
    editor_agent = create_editor_agent()
    
    return SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )


async def run_sequential_workflow():
    """Run the sequential blog creation workflow."""
    print("=" * 70)
    print("Sequential Agent: Blog Creation Pipeline")
    print("=" * 70)
    print("\nWorkflow:")
    print("  Step 1: OutlineAgent   → Creates outline")
    print("  Step 2: WriterAgent    → Writes draft from outline")
    print("  Step 3: EditorAgent    → Polishes draft")
    print("\n" + "=" * 70)
    
    # Create the pipeline
    pipeline = create_blog_pipeline()
    
    # Create runner
    runner = InMemoryRunner(agent=pipeline)
    
    # Test topic
    topic = "Write a blog post about the benefits of multi-agent systems for software developers"
    
    print(f"\nTopic: {topic}\n")
    print("Processing pipeline...")
    print("─" * 70)
    
    response = await runner.run_debug(topic)
    
    print("\n" + "=" * 70)
    print("Pipeline complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_sequential_workflow())
