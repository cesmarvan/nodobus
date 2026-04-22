"""Pydantic schemas for Autobus model."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from .geometry_utils import wkbelement_to_geojson


class AutobusBase(BaseModel):
    """Base schema for Autobus with common fields."""
    
    vehiculo: int = Field(..., description="Vehicle identifier")
    posicion: dict = Field(
        ...,
        description="Geographic Point geometry representing the current location",
        example={
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]  # [longitude, latitude]
        }
    )
    sentido: int = Field(..., description="Direction of travel (1 or 2)")
    linea_id: int = Field(..., description="Foreign key reference to the Linea")


class AutobusCreate(AutobusBase):
    """Schema for creating a new Autobus."""
    pass


class AutobusUpdate(BaseModel):
    """Schema for updating an existing Autobus."""
    
    posicion: Optional[dict] = Field(None, description="Geographic Point geometry representing the current location")
    sentido: Optional[int] = Field(None, description="Direction of travel (1 or 2)")
    linea_id: Optional[int] = Field(None, description="Foreign key reference to the Linea")


class AutobusResponse(AutobusBase):
    """Schema for Autobus response."""
    
    id: int = Field(..., description="Primary key identifier")
    
    @field_validator('posicion', mode='before')
    @classmethod
    def validate_posicion(cls, v: Any) -> dict:
        """Convert WKBElement to GeoJSON before validation."""
        if isinstance(v, dict):
            return v
        # If it's a WKBElement from the database, convert it
        return wkbelement_to_geojson(v)
    
    class Config:
        from_attributes = True
