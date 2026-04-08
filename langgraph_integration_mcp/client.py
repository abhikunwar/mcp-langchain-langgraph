import langchain_core
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
import asyncio
from langchain_core.messages import AIMessage
load_dotenv()
model = ChatGroq(temperature=0.5, model="llama-3.1-8b-instant",max_tokens = 50,model_kwargs={'seed':8})
# Llama-3.3-70b-specdec
# llama-3.1-8b-instant
class WeatherAgent:
    def __init__(self):
        self.client = MultiServerMCPClient({
            "weather": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:3000/mcp/",
            }
        })
    
    async def get_weather_tools(self):
        return await self.client.get_tools()
    
    async def ask_weather(self, question: str):
        tools = await self.get_weather_tools()
        agent = create_agent(model, tools)
        return await agent.ainvoke({"messages": question})

async def main():
    agent = WeatherAgent()
    result = await agent.ask_weather("How will the weather be in Munich today?")
    messages = result["messages"]
    print("ALL MESSAGES:", messages)
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            print("Agent response:", msg.content)
            break
    else:
        print("No AIMessage found.")

if __name__=="__main__":
    asyncio.run(main())
