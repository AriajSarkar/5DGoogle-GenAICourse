"""
Day 4b: Agent Evaluation - CLI-Based Regression Testing

This script demonstrates automated regression testing using adk eval CLI command.
Shows how to create evaluation configs, test cases, and run batch evaluations.

Learning Objectives:
- Create evaluation configuration (test_config.json)
- Create test cases programmatically (*.evalset.json)
- Run CLI evaluation for batch testing
- Analyze detailed results to identify failures

Key Concepts:
1. Evaluation Config: Define pass/fail thresholds (test_config.json)
2. Test Cases: JSON file with user prompts, expected responses, expected tools
3. CLI Evaluation: adk eval agent/ evalset.json --config_file_path
4. Result Analysis: Response match scores, tool trajectory scores, detailed diffs

Run this script:
    python Day4/4b-agent-evaluation/02_cli_evaluation.py

For actual CLI evaluation:
    adk eval Day4/4b-agent-evaluation/regression_testing/ Day4/4b-agent-evaluation/regression_testing/integration.evalset.json --config_file_path=Day4/4b-agent-evaluation/regression_testing/test_config.json --print_detailed_results
"""

import asyncio
import json
from pathlib import Path

# This script demonstrates the file-based evaluation approach
# For actual evaluation, use: adk eval [agent_path] [evalset_path] --config_file_path [config_path]


async def main():
    print("📊 Day 4b: CLI-Based Regression Testing")
    print("=" * 60)
    print()
    print("📋 Scenario: Automated regression testing for home automation agent")
    print("🎯 Goal: Detect performance degradation over time")
    print("🔧 Tool: adk eval CLI command")
    print()
    
    # Step 1: Show evaluation configuration
    print("=" * 60)
    print("📝 STEP 1: Create Evaluation Configuration")
    print("=" * 60)
    print()
    
    eval_config = {
        "criteria": {
            "tool_trajectory_avg_score": 1.0,  # Perfect tool usage required
            "response_match_score": 0.8,  # 80% text similarity threshold
        }
    }
    
    print("File: test_config.json")
    print(json.dumps(eval_config, indent=2))
    print()
    print("📊 What these criteria mean:")
    print("  • tool_trajectory_avg_score: 1.0 - Exact tool usage match required")
    print("  • response_match_score: 0.8 - 80% text similarity required")
    print()
    print("🎯 What this catches:")
    print("  ✅ Incorrect tool usage (wrong device, location, or status)")
    print("  ✅ Poor response quality and communication")
    print("  ✅ Deviations from expected behavior patterns")
    print()
    
    # Step 2: Show test cases
    print("=" * 60)
    print("📝 STEP 2: Create Test Cases")
    print("=" * 60)
    print()
    
    test_cases = {
        "eval_set_id": "regression_test_suite",
        "eval_cases": [
            {
                "eval_id": "basic_light_control",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "Turn on the desk lamp in the office"}]
                        },
                        "final_response": {
                            "parts": [
                                {"text": "Successfully set the desk lamp in the office to on."}
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "office",
                                        "device_id": "desk lamp",
                                        "status": "ON",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "eval_id": "bedroom_light_off",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "Turn off the ceiling light in the bedroom"}]
                        },
                        "final_response": {
                            "parts": [
                                {"text": "Successfully set the ceiling light in the bedroom to off."}
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "bedroom",
                                        "device_id": "ceiling light",
                                        "status": "OFF",
                                    },
                                }
                            ]
                        },
                    }
                ],
            },
        ],
    }
    
    print("File: integration.evalset.json")
    print(json.dumps(test_cases, indent=2)[:500] + "...")
    print()
    print("🧪 Test scenarios:")
    for case in test_cases["eval_cases"]:
        user_msg = case["conversation"][0]["user_content"]["parts"][0]["text"]
        print(f"  • {case['eval_id']}: {user_msg}")
    print()
    
    # Step 3: Show CLI command
    print("=" * 60)
    print("📝 STEP 3: Run CLI Evaluation")
    print("=" * 60)
    print()
    print("Command:")
    print("  adk eval \\")
    print("    Day4/4b-agent-evaluation/regression_testing/ \\")
    print("    Day4/4b-agent-evaluation/regression_testing/integration.evalset.json \\")
    print("    --config_file_path=Day4/4b-agent-evaluation/regression_testing/test_config.json \\")
    print("    --print_detailed_results")
    print()
    print("What this does:")
    print("  1. Loads agent from regression_testing/ directory")
    print("  2. Loads test cases from integration.evalset.json")
    print("  3. Loads evaluation criteria from test_config.json")
    print("  4. Runs each test case")
    print("  5. Compares actual vs expected (response + tool usage)")
    print("  6. Prints detailed pass/fail report")
    print()
    
    # Step 4: Show sample results
    print("=" * 60)
    print("📝 STEP 4: Analyze Results")
    print("=" * 60)
    print()
    print("Sample output:")
    print()
    print("*********************************************************************")
    print("Eval Run Summary")
    print("regression_test_suite:")
    print("  Tests passed: 1")
    print("  Tests failed: 1")
    print("********************************************************************")
    print()
    print("Eval Set Id: regression_test_suite")
    print("Eval Id: basic_light_control")
    print("Overall Eval Status: PASSED")
    print("---------------------------------------------------------------------")
    print("Metric: tool_trajectory_avg_score, Status: PASSED, Score: 1.0, Threshold: 1.0")
    print("Metric: response_match_score, Status: PASSED, Score: 0.95, Threshold: 0.8")
    print("---------------------------------------------------------------------")
    print()
    print("Eval Id: bedroom_light_off")
    print("Overall Eval Status: FAILED")
    print("---------------------------------------------------------------------")
    print("Metric: tool_trajectory_avg_score, Status: PASSED, Score: 1.0, Threshold: 1.0")
    print("Metric: response_match_score, Status: FAILED, Score: 0.65, Threshold: 0.8")
    print("---------------------------------------------------------------------")
    print()
    print("📊 Analysis:")
    print("  Test 1 (basic_light_control):")
    print("    ✅ PASSED - Perfect tool usage (1.0), great response (0.95)")
    print()
    print("  Test 2 (bedroom_light_off):")
    print("    ❌ FAILED - Perfect tool usage (1.0), poor response (0.65 < 0.8)")
    print("    ROOT CAUSE: Response text too different from expected")
    print("    FIX: Update agent instruction for more consistent language")
    print()
    
    # Step 5: Best practices
    print("=" * 60)
    print("🎯 BEST PRACTICES")
    print("=" * 60)
    print()
    print("1. Test Creation:")
    print("   • Start with ADK web UI to create test cases interactively")
    print("   • Download evalsets from UI for baseline")
    print("   • Add edge cases programmatically")
    print()
    print("2. Thresholds:")
    print("   • tool_trajectory: Usually 1.0 (exact match)")
    print("   • response_match: 0.7-0.9 (allow some variation)")
    print("   • Adjust based on your requirements")
    print()
    print("3. Regression Testing:")
    print("   • Run evaluations after every agent change")
    print("   • Track metrics over time (trending)")
    print("   • Fail CI/CD pipeline if tests fail")
    print()
    print("4. Test Coverage:")
    print("   • Happy path scenarios")
    print("   • Edge cases (ambiguous commands, invalid locations)")
    print("   • Error handling (missing parameters)")
    print()
    print("=" * 60)
    print("✅ Next Steps:")
    print("   1. Run the actual CLI command above")
    print("   2. Examine detailed results with --print_detailed_results")
    print("   3. Fix any failing tests by updating agent instructions")
    print("   4. Re-run evaluation to verify fixes")
    print("   5. See 03_user_simulation.py for dynamic test generation")


if __name__ == "__main__":
    asyncio.run(main())
