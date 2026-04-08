# test_sse_client.py - Test your running SSE server

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def test_sse():
    print("Connecting to MCP server at http://localhost:8000/sse...")
    
    try:
        async with sse_client("http://localhost:8000/sse") as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ Connected and initialized!")
                
                # List all tools
                tools = await session.list_tools()
                print(f"\n📋 Found {len(tools.tools)} tool(s):")
                for tool in tools.tools:
                    print(f"   🔧 {tool.name}: {tool.description}")
                
                # Test the hello tool
                print("\n📞 Calling 'hello' tool...")
                result = await session.call_tool("hello", arguments={"name": "GKE Student"})
                print(f"   Response: {result.content[0].text}")
                
                # Test the add tool
                print("\n📞 Calling 'add' tool...")
                result = await session.call_tool("add", arguments={"a": 25, "b": 17})
                print(f"   Response: {result.content[0].text}")
                
                print("\n✨ All tests passed! Your MCP server is ready for GKE!")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure server.py is running in another terminal")
        print("2. Check that server shows 'Uvicorn running on http://127.0.0.1:8000'")
        print("3. Try curl http://localhost:8000/sse to test connectivity")

if __name__ == "__main__":
    asyncio.run(test_sse())

