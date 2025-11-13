"""
Day 4b: Agent Evaluation - Interactive Testing with ADK Web UI

This script demonstrates interactive test case creation and evaluation.
Shows how to use ADK web UI for creating, running, and analyzing evaluations.

Learning Objectives:
- Create test cases from conversations in ADK web UI
- Run evaluations with response_match and tool_trajectory metrics
- Analyze pass/fail results in Evaluation History
- Understand evaluation as proactive quality assurance

Key Concepts:
1. Test Case Creation: Save successful conversations as evaluation cases
2. Evaluation Metrics: response_match (text similarity), tool_trajectory (correct tools/params)
3. Interactive Analysis: Side-by-side comparison in web UI
4. Regression Detection: Re-run tests to ensure consistent behavior

Note: This script guides you through the ADK web UI workflow.
For programmatic evaluation, see 02_cli_evaluation.py

Run in development environment:
    1. adk web Day4/4b-agent-evaluation/
    2. Select home_automation_eval from the agent dropdown
    3. Have a conversation: "Turn on the desk lamp in the office"
    3. Save as test case in Eval tab
    4. Run evaluation and analyze results
"""

import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from google.genai import types
from utils.model_config import get_text_model

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


def set_device_status(location: str, device_id: str, status: str) -> dict:
    """
    Sets the status of a smart home device.
    
    Args:
        location: The room where the device is located.
        device_id: The unique identifier for the device.
        status: The desired status, either 'ON' or 'OFF'.
    
    Returns:
        A dictionary confirming the action.
    """
    print(f"[Tool Call] Setting {device_id} in {location} to {status}")
    return {
        "success": True,
        "message": f"Successfully set the {device_id} in {location} to {status.lower()}."
    }


async def main():
    print("📝 Day 4b: Interactive Agent Evaluation")
    print("=" * 60)
    print()
    print("📋 Scenario: Home Automation Agent")
    print("🎯 Goal: Create and run test cases interactively")
    print("🔧 Tool: ADK Web UI Evaluation Features")
    print()
    print("=" * 60)
    print("📚 INTERACTIVE WEB UI WORKFLOW")
    print("=" * 60)
    print()
    print("Step 1: Create Test Cases")
    print("  1. Run: adk web Day4/4b-agent-evaluation/")
    print("  2. Select home_automation_eval from the agent dropdown")
    print("  3. Have a conversation: 'Turn on the desk lamp in the office'")
    print("  3. Click Eval tab → Create Evaluation set → Name it 'home_tests'")
    print("  4. Click '>' arrow → Add current session")
    print("  5. Give it case name: 'basic_device_control'")
    print()
    print("Step 2: Run Evaluation")
    print("  1. In Eval tab, check your test case")
    print("  2. Click 'Run Evaluation' button")
    print("  3. EVALUATION METRIC dialog appears")
    print("  4. Leave default values, click 'Start'")
    print("  5. See green 'Pass' in Evaluation History")
    print()
    print("Step 3: Analyze Failure (Practice)")
    print("  1. Edit test case (pencil icon)")
    print("  2. Change expected response to: 'The desk lamp is off.'")
    print("  3. Re-run evaluation")
    print("  4. See red 'Fail' result")
    print("  5. Hover over 'Fail' → See Actual vs Expected comparison")
    print()
    print("=" * 60)
    print("📊 EVALUATION METRICS EXPLAINED")
    print("=" * 60)
    print()
    print("1. response_match_score:")
    print("   • Measures text similarity between actual and expected response")
    print("   • Score 1.0 = perfect match, 0.0 = completely different")
    print("   • Threshold: 0.8 (80% similarity required to pass)")
    print()
    print("2. tool_trajectory_avg_score:")
    print("   • Measures correct tool usage with correct parameters")
    print("   • Score 1.0 = exact tool match, 0.0 = wrong tools/params")
    print("   • Threshold: 1.0 (perfect tool usage required)")
    print()
    print("=" * 60)
    print("🎯 WHY EVALUATION MATTERS")
    print("=" * 60)
    print()
    print("❌ Problem 1: Production Deployment")
    print("   • Manual testing doesn't scale")
    print("   • Agent works in dev, fails in production")
    print("   • No way to catch regressions")
    print()
    print("✅ Solution: Systematic Evaluation")
    print("   • Automated test cases catch regressions")
    print("   • Response & trajectory metrics ensure quality")
    print("   • Re-run tests after every change")
    print()
    print("❌ Problem 2: Non-Deterministic Agents")
    print("   • Agents give different answers each time")
    print("   • Small prompt changes cause big behavior shifts")
    print("   • Hard to know if agent improved or degraded")
    print()
    print("✅ Solution: Evaluation Metrics")
    print("   • tool_trajectory catches wrong tool usage")
    print("   • response_match detects communication quality issues")
    print("   • Thresholds define acceptable variance")
    print()
    print("=" * 60)
    print("🧪 PROGRAMMATIC EXAMPLE")
    print("=" * 60)
    print()
    print("For automated testing outside the web UI, see:")
    print("  • 02_cli_evaluation.py - Batch testing with adk eval CLI")
    print("  • 03_user_simulation.py - Dynamic test case generation")
    print()
    
    # Create agent for reference
    agent = LlmAgent(
        model=Gemini(model=get_text_model(), retry_options=retry_config),
        name="home_automation_agent",
        description="An agent to control smart devices in a home.",
        instruction="""You are a home automation assistant. You control smart devices.
        
        When the user asks to control a device, use the set_device_status tool with the exact location,
        device_id, and status (ON or OFF) specified by the user.
        
        Respond with a confirmation message.""",
        tools=[set_device_status],
    )
    
    runner = InMemoryRunner(agent=agent)
    
    print("🚀 Running agent programmatically (for reference)...")
    print()
    
    response = await runner.run_debug("Turn on the desk lamp in the office")
    
    print()
    print("="*60)
    print("✅ Next Steps:")
    print("   1. Open ADK web UI: adk web Day4/4b-agent-evaluation/")
    print("   2. Select home_automation_eval from the dropdown")
    print("   3. Create test cases from successful conversations")
    print("   3. Run evaluations to establish baseline")
    print("   4. Re-run tests after making changes to detect regressions")


if __name__ == "__main__":
    asyncio.run(main())
