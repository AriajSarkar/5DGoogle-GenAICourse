"""
MCP Image Agent - Day 2b: Model Context Protocol Integration
Based on Kaggle 5-Day Agents Course - Day 2b
Copyright 2025 Google LLC - Licensed under Apache 2.0

Demonstrates:
- Model Context Protocol (MCP) integration
- Using external MCP servers as tools
- Connecting to community-built integrations
- McpToolset configuration

NOTE: Requires Node.js/npm installed for MCP server
"""

from utils.model_config import get_multimodal_model

from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Configure retry options
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# MCP Toolset - connects to Everything MCP Server
# This server provides getTinyImage tool for testing MCP integration
# NOTE: On Windows, npx must be called as npx.cmd
import platform
npx_command = "npx.cmd" if platform.system() == "Windows" else "npx"

mcp_image_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=npx_command,  # Windows uses npx.cmd, Unix uses npx
            args=[
                "-y",  # Auto-confirm install
                "@modelcontextprotocol/server-everything",
            ],
            tool_filter=["getTinyImage"],  # Only use this specific tool
        ),
        timeout=30,
    )
)

# Create image agent with MCP integration
root_agent = LlmAgent(
    model=Gemini(model=get_multimodal_model(), retry_options=retry_config),
    name="image_agent",
    instruction="""You are an image generation assistant.
    
    When users request images:
    1. Use the MCP tool getTinyImage to generate a sample tiny image
    2. Explain that this is a test image (16x16 pixels)
    3. In production, you would connect to real image generation services
    
    The getTinyImage tool returns base64-encoded image data.
    """,
    tools=[mcp_image_server],
)

# NOTE: To display the image in production:
# 1. Extract base64 data from tool response
# 2. Decode: base64.b64decode(image_data)
# 3. Display using your framework (Flask, FastAPI, etc.)
