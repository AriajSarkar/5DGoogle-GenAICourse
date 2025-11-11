"""
1b - Sequential Agents: The Assembly Line Pattern (ADK App Structure)
======================================================================
This is the ADK-compatible version of 02_sequential_pattern.py

To run this with ADK CLI:
    adk run Day1/1b-agent-architectures/02_sequential_pattern

Concepts covered:
- SequentialAgent for guaranteed execution order
- Pipeline workflows (Outline → Write → Edit)
- State passing between agents with output_key
- Fixed, predictable workflows in ADK app structure
"""

from google.adk.agents import Agent, SequentialAgent


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


# Root agent: Sequential pipeline (Outline → Write → Edit)
root_agent = SequentialAgent(
    name="BlogPipeline",
    sub_agents=[
        create_outline_agent(),
        create_writer_agent(),
        create_editor_agent(),
    ],
)
