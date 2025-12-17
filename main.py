from mcp.server.fastmcp import FastMCP
from server import create_sse_server
import uvicorn

# Import all the conversion functions
from tools.TLC_address import tlc_to_address
from tools.address_TLC import address_to_tlc
from tools.address_plasma import address_to_plasma
from tools.plasma_address import plasma_to_address

# Initialize FastMCP server
mcp = FastMCP("Quadrant Coordinate Converter")

@mcp.tool()
def tlc_to_address_tool(tlc: str) -> str:
    """
    Convert TLC (Tile-based Location Code) to a human-readable address.
    
    Args:
        tlc: The TLC code to convert (e.g., '123-456-78')
    
    Returns:
        A human-readable address corresponding to the TLC code
    """
    try:
        result = tlc_to_address(tlc)
        return f"Address: {result}"
    except Exception as e:
        return f"Error converting TLC to address: {str(e)}"

@mcp.tool()
def address_to_tlc_tool(address: str) -> str:
    """
    Convert a human-readable address to TLC (Tile-based Location Code).
    
    Args:
        address: The address to convert to TLC
    
    Returns:
        The TLC code corresponding to the address
    """
    try:
        result = address_to_tlc(address)
        return f"TLC: {result}"
    except Exception as e:
        return f"Error converting address to TLC: {str(e)}"

@mcp.tool()
def address_to_plasma_tool(address: str) -> str:
    """
    Convert a human-readable address to Plasma coordinate format.
    
    Args:
        address: The address to convert to Plasma format
    
    Returns:
        The Plasma coordinate representation of the address
    """
    try:
        result = address_to_plasma(address)
        return f"Plasma: {result}"
    except Exception as e:
        return f"Error converting address to Plasma: {str(e)}"

@mcp.tool()
def plasma_to_address_tool(plasma: str) -> str:
    """
    Convert Plasma coordinate format to a human-readable address.
    
    Args:
        plasma: The Plasma coordinate to convert (e.g., 'plasma://40.7128,-74.0060')
    
    Returns:
        A human-readable address corresponding to the Plasma coordinate
    """
    try:
        result = plasma_to_address(plasma)
        return f"Address: {result}"
    except Exception as e:
        return f"Error converting Plasma to address: {str(e)}"

# Create the SSE server using your app.py function
app = create_sse_server(mcp)

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)