# server.py - Working MCP server
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-server")

@mcp.tool()
def hello(name: str) -> str:
    """Simple greeting tool"""
    return f"Hello {name}! MCP is working on GKE!"

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    # This works locally - we'll modify for GKE
    mcp.run(transport="sse")