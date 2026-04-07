import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    url = "http://127.0.0.1:8000/mcp/"
    async with streamable_http_client(url) as (read,write,get_Session_id):
        async with ClientSession(read,write) as session:
            
            print("before initilization",get_Session_id())
            await session.initialize()
            sid = get_Session_id()
            print("session id after session initilize",sid)
            result = await session.call_tool("add_tool",{"a": 21, "b": 21})
            print("Server Result:",result)

if __name__ == "__main__":
    asyncio.run(main())