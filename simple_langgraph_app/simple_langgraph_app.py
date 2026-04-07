# simple_langgraph_working.py - Simple LangGraph with your working MCP
import asyncio
import requests
import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
import os

# Your working MCP URL (same as test_gke_debug.py)
MCP_URL = os.environ.get("MCP_URL", "http://mcp-server-service/mcp")

# Define the state
class State(TypedDict):
    user_input: str
    tool_name: str
    tool_args: dict
    result: str
    final_output: str

# Function to call MCP (same working code from your test)
def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Call MCP tool using the working pattern from test_gke_debug.py"""
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream'
    }
    
    # Step 1: Initialize session
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "langgraph", "version": "1.0"}
        }
    }
    
    response = requests.post(MCP_URL, headers=headers, json=init_payload)
    session_id = response.headers.get('mcp-session-id')
    
    if not session_id:
        return "Error: Could not initialize session"
    
    # Step 2: Send initialized notification
    headers['Mcp-Session-Id'] = session_id
    notify_payload = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    requests.post(MCP_URL, headers=headers, json=notify_payload)
    
    # Step 3: Call the tool
    call_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    response = requests.post(MCP_URL, headers=headers, json=call_payload)
    
    # Parse the response
    for line in response.text.split('\n'):
        if line.startswith('data: '):
            data = json.loads(line[6:])
            if 'result' in data:
                return data['result']['content'][0]['text']
            elif 'error' in data:
                return f"Tool error: {data['error']}"
    
    return "No response from tool"

# Node 1: Understand what user wants
def understand_intent(state: State) -> State:
    """Decide which tool to call based on user input"""
    user_input = state["user_input"].lower()
    
    if "hello" in user_input or "hi" in user_input:
        return {
            **state,
            "tool_name": "hello",
            "tool_args": {"name": "LangGraph User"}
        }
    elif "add" in user_input or "plus" in user_input or "calculate" in user_input:
        # Simple extraction of numbers (for demo)
        words = user_input.split()
        numbers = [int(w) for w in words if w.isdigit()]
        if len(numbers) >= 2:
            a, b = numbers[0], numbers[1]
        else:
            a, b = 10, 20  # defaults
        return {
            **state,
            "tool_name": "add",
            "tool_args": {"a": a, "b": b}
        }
    else:
        return {
            **state,
            "tool_name": "hello",
            "tool_args": {"name": "Friend"}
        }

# Node 2: Execute the MCP tool
def execute_tool(state: State) -> State:
    """Call the MCP tool on GKE"""
    result = call_mcp_tool(state["tool_name"], state["tool_args"])
    return {**state, "result": result}

# Node 3: Format the final response
def format_response(state: State) -> State:
    """Create final output"""
    return {
        **state,
        "final_output": f"🤖 {state['result']}"
    }

# Build the graph
def create_agent():
    builder = StateGraph(State)
    
    builder.add_node("understand", understand_intent)
    builder.add_node("execute", execute_tool)
    builder.add_node("format", format_response)
    
    builder.set_entry_point("understand")
    builder.add_edge("understand", "execute")
    builder.add_edge("execute", "format")
    builder.add_edge("format", END)
    
    return builder.compile()

# Run the agent
def main():
    print("=" * 50)
    print("🤖 Simple LangGraph Agent with MCP on GKE")
    print("=" * 50)
    
    agent = create_agent()
    
    # Test cases
    test_inputs = [
        "Say hello to me",
        "Add 15 and 30",
        "Hi there",
        "Calculate 100 plus 50"
    ]
    
    for test_input in test_inputs:
        print(f"\n📝 User: {test_input}")
        result = agent.invoke({"user_input": test_input})
        print(f"   {result['final_output']}")
    
    print("\n" + "=" * 50)
    print("✅ Done! LangGraph successfully called MCP on GKE")

if __name__ == "__main__":
    main()