# Day 2a: Agent Tools

## Learning Objectives

Learn how to transform Python functions into powerful agent tools and build multi-tool systems.

### Key Concepts Covered

1. **Custom Function Tools** - Turn any Python function into an agent tool
2. **Structured Returns** - Use dictionaries with status fields for reliable error handling
3. **Agent as Tool** - Wrap specialist agents with `AgentTool` for delegation
4. **Code Execution** - Use `BuiltInCodeExecutor` for reliable calculations
5. **Multi-Tool Coordination** - Combine multiple tools in a single agent

## Prerequisites

- Completed Day 1 (Basic Agents and Multi-Agent Systems)
- Understanding of Python functions, type hints, and docstrings
- Google API key configured in `.env`

## ADK Apps

### 1. Currency Converter (`currency_converter/`)

Basic currency conversion agent demonstrating custom function tools.

**Tools Used:**
- `get_fee_for_payment_method()` - Lookup transaction fees
- `get_exchange_rate()` - Get currency conversion rates

**Run:**
```powershell
adk run Day2/2a-agent-tools/currency_converter
```

**Try:**
- "Convert 500 USD to EUR using platinum credit card"
- "I want to convert 1000 USD to JPY with bank transfer"

### 2. Enhanced Currency Converter (`enhanced_currency_converter/`)

Advanced version using agent delegation for precise calculations.

**Architecture:**
- Main Agent: Currency conversion logic
- Calculation Agent: Python code generation + execution
- Pattern: Agent as Tool (AgentTool wrapper)

**Run:**
```powershell
adk run Day2/2a-agent-tools/enhanced_currency_converter
```

**Try:**
- "Convert 1,250 USD to INR using Bank Transfer. Show precise calculation."
- "Convert 3,500 USD to EUR with gold debit card"

## ADK Best Practices Demonstrated

### 1. Dictionary Returns
```python
# Good - Structured with status
return {"status": "success", "fee_percentage": 0.02}
return {"status": "error", "error_message": "Not found"}

# Bad - Unclear results
return 0.02
return None
```

### 2. Clear Docstrings
```python
def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Looks up and returns the exchange rate between two currencies.
    
    Args:
        base_currency: The ISO 4217 currency code (e.g., "USD").
        target_currency: The ISO 4217 currency code (e.g., "EUR").
    
    Returns:
        Dictionary with status and rate information.
    """
```

The LLM reads this docstring to understand when and how to use the tool!

### 3. Type Hints
```python
# Required for ADK to generate proper schemas
def get_fee_for_payment_method(method: str) -> dict:
    ...
```

### 4. Error Handling
```python
# Check status in agent instructions
if tool_result["status"] == "error":
    print(tool_result["error_message"])
```

## Tool Development Workflow

1. **Create Python Function**
   - Add type hints to all parameters and return value
   - Write comprehensive docstring (LLM uses this!)
   - Return structured dictionaries

2. **Test Function Independently**
   ```python
   print(get_fee_for_payment_method('platinum credit card'))
   # {'status': 'success', 'fee_percentage': 0.02}
   ```

3. **Add to Agent**
   ```python
   agent = LlmAgent(
       tools=[get_fee_for_payment_method, get_exchange_rate],
       ...
   )
   ```

4. **Update Instructions**
   - Reference tools by exact function name
   - Tell agent when to use each tool
   - Explain how to handle errors

## Agent as Tool Pattern

When one agent should delegate to a specialist:

```python
# Create specialist agent
calculation_agent = LlmAgent(
    name="CalculationAgent",
    instruction="Generate Python code for calculations",
    code_executor=BuiltInCodeExecutor(),
)

# Use as tool in main agent
main_agent = LlmAgent(
    tools=[AgentTool(agent=calculation_agent)],
    ...
)
```

**When to use:**
- Delegation for specific tasks (calculations, translations, etc.)
- Specialist stays in background, main agent continues conversation
- Different from sub-agents (which take over completely)

## Code Execution Pattern

Why use code execution for math?

- ❌ LLMs can make calculation errors
- ❌ Inconsistent formulas across calls
- ✅ Python code is deterministic and reliable

```python
agent = LlmAgent(
    code_executor=BuiltInCodeExecutor(),  # Runs code in sandbox
    instruction="Generate Python code to calculate...",
)
```

## Common Issues

### Tool Not Being Called

**Problem:** Agent ignores your tool
**Solutions:**
- Check docstring is clear and descriptive
- Verify type hints are present
- Update agent instructions to reference the tool
- Use `run_debug()` to see tool discovery

### Calculation Errors

**Problem:** Agent makes math mistakes
**Solution:** Use `BuiltInCodeExecutor` to run Python code instead

### Unclear Error Messages

**Problem:** Tool fails but agent doesn't know why
**Solution:** Return structured errors:
```python
return {
    "status": "error",
    "error_message": "Clear explanation of what went wrong"
}
```

## Comparison: Kaggle vs Our Implementation

| Aspect | Kaggle Version | Our Version |
|--------|---------------|-------------|
| Environment | Jupyter Notebook | ADK App (agent.py + __init__.py) |
| Model | gemini-2.5-flash-lite | gemini-2.5-flash |
| API Key | Kaggle Secrets | .env file |
| Execution | Cell-by-cell | Interactive CLI / Web UI |
| Structure | Inline code | Production-ready modules |

## Next Steps

Continue to **Day 2b: Agent Tool Patterns and Best Practices** to learn:
- MCP (Model Context Protocol) integration
- Long-running operations with human-in-the-loop
- Resumable workflows

## Learn More

- [ADK Tools Documentation](https://googleapis.github.io/agent-developer-kit/docs/tools/)
- [ADK Function Tools Guide](https://googleapis.github.io/agent-developer-kit/docs/tools/function-tools/)
- [Built-in Code Executor](https://googleapis.github.io/agent-developer-kit/docs/tools/built-in-tools/#code-executor)

---

**Authors:** Laxmi Harikumar (Kaggle Course), Adapted for ADK by Course Team
**License:** Apache 2.0
