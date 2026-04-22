"""Utilities for converting between geometry formats."""

from typing import Any, Dict


def wkbelement_to_geojson(wkbelement: Any) -> Dict[str, Any]:
    """Convert a WKBElement to GeoJSON format.
    
    Args:
        wkbelement: A GeoAlchemy2 WKBElement object
        
    Returns:
        A GeoJSON dictionary with 'type' and 'coordinates'
    """
    try:
        from shapely.wkb import loads as wkb_loads
        from shapely.geometry import mapping
        
        # Extract binary WKB data from WKBElement
        if hasattr(wkbelement, 'data'):
            wkb_data = wkbelement.data
        else:
            raise AttributeError("WKBElement has no 'data' attribute")
        
        # wkb_data could be bytes already, or it might be a memoryview
        if isinstance(wkb_data, memoryview):
            wkb_data = bytes(wkb_data)
        elif not isinstance(wkb_data, bytes):
            # Try to convert to bytes if it's something else
            wkb_data = bytes(wkb_data)
        
        # Use shapely to load WKB and convert to GeoJSON using mapping()
        shape = wkb_loads(wkb_data)
        geojson_dict = mapping(shape)
        return geojson_dict
    
    except Exception as e:
        # Debug info: show what we got
        raise ValueError(f"Could not convert WKBElement to GeoJSON: {str(e)}")
