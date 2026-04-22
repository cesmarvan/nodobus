"""Pydantic schemas for Parada model."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from .geometry_utils import wkbelement_to_geojson


class ParadaBase(BaseModel):
    """Base schema for Parada with common fields."""
    
    nodo: int = Field(..., description="Integer identifier for the node")
    nombre: str = Field(..., description="Name of the stop", max_length=255)
    localizacion: dict = Field(
        ...,
        description="Geographic point location (GeoJSON Point)",
        example={
            "type": "Point",
            "coordinates": [-73.935242, 40.730610]  # [longitude, latitude]
        }
    )


class ParadaCreate(ParadaBase):
    """Schema for creating a new Parada."""
    pass


class ParadaUpdate(BaseModel):
    """Schema for updating an existing Parada."""
    
    nodo: Optional[int] = Field(None, description="Integer identifier for the node")
    nombre: Optional[str] = Field(None, description="Name of the stop", max_length=255)
    localizacion: Optional[dict] = Field(
        None,
        description="Geographic point location (GeoJSON Point)"
    )


class ParadaResponse(ParadaBase):
    """Schema for Parada response."""
    
    id: int = Field(..., description="Primary key identifier")
    
    @field_validator('localizacion', mode='before')
    @classmethod
    def validate_localizacion(cls, v: Any) -> dict:
        """Convert WKBElement to GeoJSON before validation."""
        if isinstance(v, dict):
            return v
        # If it's a WKBElement from the database, convert it
        return wkbelement_to_geojson(v)
    
    class Config:
        from_attributes = True
