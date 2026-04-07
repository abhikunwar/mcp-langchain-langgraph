# server_docker_patch.py - Alternative approach

from mcp.server.fastmcp import FastMCP
# from mcp.server.fastmcp.server import Transport
import uvicorn
import os

mcp = FastMCP("test-server")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello {name}! MCP in Docker!"

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
     # ✅ CORRECT METHOD for your version
    # streamable_http_app() creates the ASGI app for GKE deployment
    app = mcp.streamable_http_app()
    
    # Run with uvicorn - host="0.0.0.0" is essential for Docker/GKE
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)