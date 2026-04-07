# server_gke.py - Fixed for GKE
from mcp.server.fastmcp import FastMCP
import uvicorn
import os

mcp = FastMCP("test-server")

@mcp.tool()
def hello(name: str) -> str:
    """Simple greeting tool"""
    return f"Hello {name}! MCP is running on GKE!"

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    # Get the ASGI app
    app = mcp.streamable_http_app()
    
    print(f"🚀 Starting MCP server on 0.0.0.0:{port}")
    print(f"📡 MCP endpoint: http://0.0.0.0:{port}/mcp")
    print(f"🔧 Available tools: hello, add")
    
    # Run with proper host header handling
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        server_header=False,
        proxy_headers=True,  # Important: Trust proxy headers
        forwarded_allow_ips="*"  # Allow all IPs (GKE LoadBalancer)
    )