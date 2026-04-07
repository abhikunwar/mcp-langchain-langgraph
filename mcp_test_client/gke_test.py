# test_gke_debug.py - Shows full response details
import requests
import json

GKE_URL = "http://localhost:8080/mcp"

print("🚀 Testing MCP Server on GKE")
print(f"📍 URL: {GKE_URL}\n")

# Step 1: Initialize session
print("1️⃣ Initializing session...")
init_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "gke-test", "version": "1.0"}
    }
}

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream'
}

response = requests.post(GKE_URL, headers=headers, json=init_payload)
session_id = response.headers.get('mcp-session-id')

print(f"   Session ID: {session_id}")
print(f"   Status Code: {response.status_code}")
print(f"   Response text: {response.text[:200]}\n")

if not session_id:
    print("⚠️ No session ID received! The server might not be ready.")
    print("   Let's check if the server is reachable...")
    
    # Test if server is reachable at all
    try:
        test_response = requests.get(GKE_URL, timeout=5)
        print(f"   GET request status: {test_response.status_code}")
    except Exception as e:
        print(f"   Connection error: {e}")
    exit()

# Step 2: Send initialized notification
print("2️⃣ Sending initialized notification...")
headers['Mcp-Session-Id'] = session_id
notify_payload = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
response2 = requests.post(GKE_URL, headers=headers, json=notify_payload)
print(f"   Status Code: {response2.status_code}\n")

# Step 3: Call hello tool
print("3️⃣ Calling 'hello' tool...")
call_payload = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "hello",
        "arguments": {"name": "GKE Student"}
    }
}
response3 = requests.post(GKE_URL, headers=headers, json=call_payload)

print(f"   Status Code: {response3.status_code}")
print(f"   Raw Response: {response3.text}")

# Parse the SSE response
print("\n4️⃣ Parsing response:")
for line in response3.text.split('\n'):
    if line.strip():
        print(f"   Line: {line}")
    if line.startswith('data: '):
        try:
            data = json.loads(line[6:])
            if 'result' in data:
                content = data['result'].get('content', [])
                if content:
                    print(f"   ✅ Tool result: {content[0].get('text', 'No text')}")
            elif 'error' in data:
                print(f"   ❌ Error: {data['error']}")
        except json.JSONDecodeError as e:
            print(f"   JSON parse error: {e}")

print("\n✨ Test complete!")