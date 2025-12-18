"""
Quadrant-based utilities for spatial search and filtering in Qdrant.
"""
from typing import List, Dict, Any, Tuple, Optional
import math

# Define quadrant boundaries (customize these based on your coordinate system)
QUADRANTS = {
    'NE': {'lat': (0, 90), 'lon': (0, 180)},     # Northeast
    'NW': {'lat': (0, 90), 'lon': (-180, 0)},    # Northwest
    'SE': {'lat': (-90, 0), 'lon': (0, 180)},    # Southeast
    'SW': {'lat': (-90, 0), 'lon': (-180, 0)},   # Southwest
}

def get_quadrant(lat: float, lon: float) -> str:
    """
    Determine the quadrant for given latitude and longitude coordinates.
    
    Args:
        lat: Latitude (-90 to 90)
        lon: Longitude (-180 to 180)
        
    Returns:
        str: Quadrant identifier ('NE', 'NW', 'SE', 'SW')
    """
    if lat >= 0:
        return 'NE' if lon >= 0 else 'NW'
    else:
        return 'SE' if lon >= 0 else 'SW'

def get_quadrant_bounds(quadrant: str) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Get the latitude and longitude boundaries for a given quadrant.
    
    Args:
        quadrant: Quadrant identifier ('NE', 'NW', 'SE', 'SW')
        
    Returns:
        Tuple containing (lat_range, lon_range) where each range is (min, max)
    """
    if quadrant not in QUADRANTS:
        raise ValueError(f"Invalid quadrant: {quadrant}. Must be one of {list(QUADRANTS.keys())}")
    
    q = QUADRANTS[quadrant]
    return q['lat'], q['lon']

def is_in_quadrant(lat: float, lon: float, quadrant: str) -> bool:
    """
    Check if given coordinates fall within the specified quadrant.
    """
    if quadrant not in QUADRANTS:
        return False
        
    q = QUADRANTS[quadrant]
    lat_ok = q['lat'][0] <= lat < q['lat'][1]
    lon_ok = q['lon'][0] <= lon < q['lon'][1]
    return lat_ok and lon_ok

def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    
    # Haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    
    # Radius of earth in kilometers
    r = 6371.0
    return c * r
