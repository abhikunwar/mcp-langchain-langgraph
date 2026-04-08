from langchain.agents.middleware.todo import TodoListMiddleware
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    vertexai=True,                    # Use Vertex AI   
    project="adk-test-new",              # Your GCP project
    location="us-central1"            # Your region
)

agent = create_agent(
    model = model,
    middleware=[TodoListMiddleware()],
    system_prompt="""You are a helpful assistant. 
    For complex tasks, use the write_todos tool to create a plan first.
    Then execute each todo step by step."""
)
result =  agent.invoke({"messages": [HumanMessage("Help me refactor my codebase")]})
print(result["messages"][-1].content)

