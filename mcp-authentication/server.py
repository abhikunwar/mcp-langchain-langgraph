import fastmcp
import os
from fastmcp import FastMCP
from fastmcp.server.auth import JWTVerifier
from dotenv import load_dotenv
load_dotenv()

AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
API_AUDIENCE = os.environ.get("API_AUDIENCE", "http://localhost:8000/mcp")
REQUIRED_SCOPES = ["read:add"]

auth = JWTVerifier(
    jwks_uri=f"{AUTH0_DOMAIN.rstrip('/')}/.well-known/jwks.json",
    issuer=AUTH0_DOMAIN.rstrip("/") + "/",
    audience=API_AUDIENCE,
    required_scopes=REQUIRED_SCOPES,
)

mcp = FastMCP(name = "secureaddserver",auth=auth)

@mcp.tool(description="add teo number")
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, stateless_http=True)




