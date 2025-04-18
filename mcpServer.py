# server.py
from mcp.server.fastmcp import FastMCP
import sys

# Initialize a new MCP server with a name (e.g., "CalculatorServer")
mcp = FastMCP("Calculator")

import math

# Define an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b








if __name__ == "__main__":
    # Check if running with mcp dev command
    print("server..started")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution