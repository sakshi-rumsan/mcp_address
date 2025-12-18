from mcp.server.fastmcp import FastMCP
from server import create_sse_server
import uvicorn
from typing import List, Dict, Any, Optional, Tuple

# Import all the conversion functions
from tools.TLC_address import tlc_to_address
from tools.address_TLC import address_to_tlc
from tools.address_plasma import address_to_plasma
from tools.plasma_address import plasma_to_address

# Import Qdrant client
from services.qdrant_client import (
    store_vectors,
    search_by_quadrant,
    search_near_location,
    search_by_filename as qdrant_search_by_filename
)

# Initialize FastMCP server
mcp = FastMCP("Quadrant Coordinate & Document Search")

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

@mcp.tool()
def store_document_chunks(
    chunks: List[str],
    filename: str,
    coordinates: Optional[Tuple[float, float]] = None
) -> Dict[str, Any]:
    """
    Store document chunks in the vector database with optional geolocation.
    
    Args:
        chunks: List of text chunks to store
        filename: Name of the source file
        coordinates: Optional tuple of (latitude, longitude) for geolocation
    
    Returns:
        Confirmation message with number of chunks stored
    """
    from sentence_transformers import SentenceTransformer
    
    try:
        # Generate embeddings
        embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        vectors = embedder.encode(chunks).tolist()
        
        # Store in Qdrant
        store_vectors(
            chunks=chunks,
            vectors=vectors,
            filename=filename,
            coordinates=coordinates
        )
        
        return {
            "status": "success",
            "chunks_stored": len(chunks),
            "filename": filename,
            "has_location": coordinates is not None
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def search_documents_by_quadrant(
    query: str,
    quadrant: str,
    top_k: int = 5,
    score_threshold: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Search for documents within a specific geographic quadrant.
    
    Args:
        query: Search query text
        quadrant: Geographic quadrant ('NE', 'NW', 'SE', 'SW')
        top_k: Maximum number of results to return
        score_threshold: Minimum similarity score (0-1)
    
    Returns:
        List of matching documents with metadata
    """
    try:
        return search_by_quadrant(
            query=query,
            quadrant=quadrant.upper(),
            top_k=top_k,
            score_threshold=score_threshold
        )
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def search_documents_near_location(
    query: str,
    latitude: float,
    longitude: float,
    radius_km: float = 10.0,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for documents near a specific location.
    
    Args:
        query: Search query text
        latitude: Center point latitude
        longitude: Center point longitude
        radius_km: Search radius in kilometers
        top_k: Maximum number of results to return
    
    Returns:
        List of matching documents with distances and metadata
    """
    try:
        return search_near_location(
            query=query,
            center_lat=latitude,
            center_lon=longitude,
            radius_km=radius_km,
            top_k=top_k
        )
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def search_documents_by_filename(
    filename: str,
    quadrant: Optional[str] = None,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for document chunks by filename, optionally filtered by quadrant.
    
    Args:
        filename: Name of the file to search for
        quadrant: Optional quadrant to filter by ('NE', 'NW', 'SE', 'SW')
        top_k: Maximum number of results to return
    
    Returns:
        List of matching document chunks with metadata
    """
    try:
        return qdrant_search_by_filename(
            filename=filename,
            quadrant=quadrant.upper() if quadrant else None,
            top_k=top_k
        )
    except Exception as e:
        return [{"error": str(e)}]

# Create the SSE server using your app.py function
app = create_sse_server(mcp)

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)