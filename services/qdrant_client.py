from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct, Filter, FieldCondition, MatchValue, Range, GeoPoint
from qdrant_client.http.models import QueryRequest, ScoredPoint
from dotenv import load_dotenv
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple

from sentence_transformers import SentenceTransformer

# Import quadrant utilities
from .quadrant_utils import get_quadrant, get_quadrant_bounds, is_in_quadrant, haversine_distance

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "documents"

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Please set QDRANT_URL and QDRANT_API_KEY in your .env")

# 🔹 Embedding model (MUST match vector size)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=False
)

# Ensure collection exists and create payload index for filename
existing = [c.name for c in client.get_collections().collections]
if COLLECTION_NAME not in existing:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance="Cosine")
    )

# 🔹 Create keyword index on "filename" for fast & allowed exact matching
# This is idempotent — safe to run every time (will skip if already exists)
try:
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="filename",
        field_schema="keyword"   # Exact string match index
    )
    print("Payload index on 'filename' created or already exists.")
except Exception as e:
    if "already exists" not in str(e).lower():
        print(f"Warning: Could not create index on filename: {e}")

def store_vectors(chunks, vectors, filename=None, coordinates: Optional[Tuple[float, float]] = None):
    """
    Store vector embeddings in Qdrant with optional metadata.
    
    Args:
        chunks: List of text chunks
        vectors: List of corresponding vector embeddings
        filename: Optional filename for the document
        coordinates: Optional tuple of (latitude, longitude) for geospatial data
    """
    points = []
    for i in range(len(chunks)):
        payload = {"text": chunks[i]}
        
        if filename:
            payload["filename"] = filename
            
        if coordinates:
            lat, lon = coordinates
            payload.update({
                "location": {"lat": lat, "lon": lon},
                "quadrant": get_quadrant(lat, lon)
            })
            
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vectors[i],
            payload=payload
        ))

    # Create geo index if it doesn't exist
    try:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="location",
            field_schema="geo"
        )
    except Exception as e:
        if "already exists" not in str(e).lower():
            print(f"Warning: Could not create geo index: {e}")

    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search_by_quadrant(
    query: str,
    quadrant: str,
    top_k: int = 10,
    score_threshold: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Search for vectors within a specific quadrant.
    
    Args:
        query: The search query text
        quadrant: The quadrant to search in ('NE', 'NW', 'SE', 'SW')
        top_k: Maximum number of results to return
        score_threshold: Minimum similarity score (0-1)
        
    Returns:
        List of matching documents with metadata
    """
    try:
        # Get quadrant boundaries
        lat_range, lon_range = get_quadrant_bounds(quadrant)
        
        # Create geo filter for the quadrant
        geo_filter = Filter(
            must=[
                FieldCondition(
                    key="location",
                    geo_bounding_box={
                        "bottom_right": {"lat": lat_range[0], "lon": lon_range[1]},
                        "top_left": {"lat": lat_range[1], "lon": lon_range[0]}
                    }
                ),
                FieldCondition(
                    key="quadrant",
                    match=MatchValue(value=quadrant)
                )
            ]
        )
        
        # Generate query vector
        query_vector = embedder.encode(query).tolist()
        
        # Search with both vector and filter
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=geo_filter,
            limit=top_k,
            score_threshold=score_threshold,
            with_payload=True,
            with_vectors=False
        )
        
        return [
            {
                "id": str(hit.id),
                "score": hit.score,
                "text": hit.payload.get("text"),
                "filename": hit.payload.get("filename"),
                "location": hit.payload.get("location"),
                "quadrant": hit.payload.get("quadrant")
            }
            for hit in search_result
        ]
        
    except Exception as e:
        print(f"Error in quadrant search: {str(e)}")
        return []

def search_near_location(
    query: str,
    center_lat: float,
    center_lon: float,
    radius_km: float = 10.0,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for vectors within a certain radius of a location.
    
    Args:
        query: The search query text
        center_lat: Center point latitude
        center_lon: Center point longitude
        radius_km: Search radius in kilometers
        top_k: Maximum number of results to return
        
    Returns:
        List of matching documents with metadata and distance from center
    """
    try:
        # Generate query vector
        query_vector = embedder.encode(query).tolist()
        
        # Create geo filter for radius search
        geo_filter = Filter(
            must=[
                FieldCondition(
                    key="location",
                    geo_radius={
                        "center": {"lat": center_lat, "lon": center_lon},
                        "radius": radius_km * 1000  # Convert km to meters
                    }
                )
            ]
        )
        
        # Search with both vector and filter
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=geo_filter,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        )
        
        # Calculate distance for each result
        results = []
        for hit in search_result:
            loc = hit.payload.get("location", {})
            if loc:
                distance_km = haversine_distance(
                    (center_lat, center_lon),
                    (loc.get("lat", 0), loc.get("lon", 0))
                )
            else:
                distance_km = None
                
            results.append({
                "id": str(hit.id),
                "score": hit.score,
                "distance_km": distance_km,
                "text": hit.payload.get("text"),
                "filename": hit.payload.get("filename"),
                "location": loc,
                "quadrant": hit.payload.get("quadrant")
            })
            
        return results
        
    except Exception as e:
        print(f"Error in location-based search: {str(e)}")
        return []

def search_by_filename(
    filename: str,
    top_k: int = 10,
    quadrant: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for all chunks belonging to a specific filename, optionally filtered by quadrant.
    
    Args:
        filename: The filename to search for
        top_k: Maximum number of results to return
        quadrant: Optional quadrant to filter by ('NE', 'NW', 'SE', 'SW')
        
    Returns:
        List of matching documents with metadata
    """
    filters = [
        FieldCondition(
            key="filename",
            match=MatchValue(value=filename)
        )
    ]
    
    if quadrant:
        filters.append(
            FieldCondition(
                key="quadrant",
                match=MatchValue(value=quadrant)
            )
        )
    
    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query_filter=Filter(must=filters) if filters else None,
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )

    return [
        {
            "id": str(point.id),
            "filename": point.payload.get("filename"),
            "text": point.payload.get("text"),
            "location": point.payload.get("location"),
            "quadrant": point.payload.get("quadrant"),
            "score": point.score if point.score is not None else None
        }
        for point in result.points
    ]

def delete_by_filename(filename: str) -> Dict[str, Any]:
    """
    Delete ALL points with the given filename directly using a filter.
    No need to first search for IDs — much faster and safer.
    """
    filename_filter = Filter(
        must=[
            FieldCondition(
                key="filename",
                match=MatchValue(value=filename)
            )
        ]
    )

    operation_result = client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=filename_filter,   # Direct filter selector
        wait=True                          # Wait for completion (recommended)
    )

    deleted_count = operation_result.points_deleted if hasattr(operation_result, 'points_deleted') else 0

    if deleted_count == 0:
        return {"status": "no_matches", "deleted_count": 0, "filename": filename}

    return {
        "status": "completed",
        "deleted_count": deleted_count,
        "filename": filename
    }
