from mcp.server.fastmcp import FastMCP
from server import create_sse_server
import uvicorn
from fastapi import Request
from fastapi.responses import JSONResponse

# Import all the conversion functions
from tools.models import (
    get_address_by_tlc,
    get_address_by_plsam,
    get_plsam_tlc_by_address
)

API_KEY = "rumsan"

# Initialize FastMCP server
mcp = FastMCP("Quadrant Coordinate & Document Search")

@mcp.tool()
def tlc_to_address_tool(tlc: str) -> str:
    try:
        result = get_address_by_tlc(tlc)
        return f"Address: {result}"
    except Exception as e:
        return f"Error converting TLC to address: {str(e)}"


@mcp.tool()
def plasma_to_address_tool(plasma: str) -> str:
    try:
        result = get_address_by_plsam(plasma)
        return f"Address: {result}"
    except Exception as e:
        return f"Error converting Plasma to address: {str(e)}"


@mcp.tool()
def plasma_tlc_to_address_tool(plasma: str) -> str:
    try:
        result = get_plsam_tlc_by_address(plasma)
        return f"Address: {result}"
    except Exception as e:
        return f"Error converting Plasma to address: {str(e)}"


# Create the SSE MCP server (FastAPI app)
app = create_sse_server(mcp)

# 🔐 OPTION 3: MCP-level API key protection
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing API key"}
        )
    return await call_next(request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
