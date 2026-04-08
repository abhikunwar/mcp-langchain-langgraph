# chat_app.py
import streamlit as st
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
import streamlit as st
from dotenv import load_dotenv
# import nest_asyncio
# nest_asyncio.apply()

load_dotenv()

model = ChatGroq(temperature=0.5, model="llama-3.1-8b-instant", max_tokens=150)

async def get_weather(question):
    client = MultiServerMCPClient({
        "weather": {
            "transport": "streamable_http",
            "url": "http://127.0.0.1:3000/mcp/",
        }
    })
    tools = await client.get_tools()
    agent = create_agent(model, tools)
    result = await agent.ainvoke({"messages": [("user", question)]})
    
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage):
            return msg.content
    return "Sorry, couldn't process"

# UI
st.title("🌤️ Weather Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about weather..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("🌤️"):
            response = asyncio.run(get_weather(prompt))
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})