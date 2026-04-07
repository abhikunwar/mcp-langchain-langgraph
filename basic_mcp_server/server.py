import mcp
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo server")

@mcp.tool(description="Add two numbers")
def add_tool(a:int,b:int):
    return a + b

if __name__=="__main__":
    mcp.run(transport="streamable-http")