from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    vertexai=True,                    # Use Vertex AI   
    project="adk-test-new",              # GCP project
    location="us-central1"            # region
)

def search(query: str) -> str:
    '''search tool'''
    return f"Results for: {query}"

def calculate(expression: str) -> float:
    '''math calculation'''
    return eval(expression)

def write_report(content: str) -> str:
    '''expert writer'''
    return f"Report: {content}"

# Create subagents
research_agent = {
    "name": "researcher",
    "description": "Gathers information from the internet",
    "system_prompt": "You are a research expert. Gather comprehensive information.",
    "tools": [search],
    "model": model,
}

math_agent = {
    "name": "calculator", 
    "description": "Performs mathematical calculations",
    "system_prompt": "You are a math expert.",
    "tools": [calculate],
    "model": model,
}

writer_agent = {
    "name": "writer",
    "description": "Creates polished reports",
    "system_prompt": "You are a expert writer.",
    "tools": [write_report],
    "model": model,
}

# Create main agent with forced sequence
agent = create_deep_agent(
    model=model,
    subagents=[research_agent, math_agent, writer_agent],
    system_prompt="""
    You are a workflow orchestrator. For complex tasks:
    
    ALWAYS follow this sequence:
    1. Use 'researcher' to gather raw information
    2. Use 'calculator' to process any numerical data
    3. Use 'writer' to create final output

    To use a subagent, call the 'task' tool with:

    Available subagents:
    - 'researcher': For gathering information
    - 'calculator': For mathematical calculations  
    - 'writer': For creating reports
    
    Never skip steps or change order.
    After each subagent completes, proceed to the next.
    """
)

# Run with a complex task
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Research AI adoption rates in 2024, calculate the average growth from 2020-2024, and write a summary report"
    }]
})

print(result)


'''
There's a confirmed compatibility issue between Gemini models and Deep Agents. When using Gemini with create_deep_agent(), the model consistently returns empty responses with a MALFORMED_FUNCTION_CALL finish reason, making the agent non-functional .

A GitHub issue (#417) in the langchain-ai/deepagents repository confirms this problem . The issue shows that:

https://github.com/langchain-ai/deepagents/issues/417
'''