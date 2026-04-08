import langchain
from langchain_community.tools import DuckDuckGoSearchResults
from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

import os
search = DuckDuckGoSearchResults()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    vertexai=True,                    # Use Vertex AI   
    project="adk-test-new",              # Your GCP project
    location="us-central1"            # Your region
)

# create one search tool
def search_tool(query:str):
    """Run a web search"""
    return search.invoke(query)

# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## 'search_tool'

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

agent = create_deep_agent(
    model=model,
    tools=[search_tool],
    system_prompt= research_instructions
)

result = agent.invoke({"messages": [{"role": "user", "content": "What is langgraph?"}]})

# Print the agent's response
print(result["messages"][-1].content)




'''How does it work?
Your deep agent automatically:
Plans its approach using the built-in write_todos tool to break down the research task.
Conducts research by calling the internet_search tool to gather information.
Manages context by using file system tools (write_file, read_file) to offload large search results.
Spawns subagents as needed to delegate complex subtasks to specialized subagents.
Synthesizes a report to compile findings into a coherent response.'''