from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Add SSE server")

@mcp.tool(description="Add two numbers")
def add_method(a:int,b:int):
    return a +b

if __name__=="__main__":
    mcp.run(transport="sse")