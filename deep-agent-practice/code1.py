import langchain
from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchResults
load_dotenv()
import os
from langchain_google_genai import ChatGoogleGenerativeAI
# it used anthropic model by default here i will use free gqor
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ADMIN/Downloads/adk-test-new-9cfc631d7db0.json"

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    vertexai=True,                    # Use Vertex AI   
    project="adk-test-new",              # Your GCP project
    location="us-central1"            # Your region
)

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_deep_agent(
    model=model,
    tools=[get_weather],
    system_prompt=" You are an helpful assistant"
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(result)