"""Pydantic schemas for Linea model."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from .geometry_utils import wkbelement_to_geojson


class LineaBase(BaseModel):
    """Base schema for Linea with common fields."""
    
    color: str = Field(..., description="Hex color code for the line", max_length=7)
    destino: str = Field(..., description="Destination of the line", max_length=255)
    labelLinea: str = Field(..., description="Label identifier for the line", max_length=50)
    linea: int = Field(..., description="Integer identifier for the line")
    nombreLinea: str = Field(..., description="Name of the line", max_length=255)
    recorrido: dict = Field(
        ...,
        description="Geographic LineString geometry representing the route",
        example={
            "type": "LineString",
            "coordinates": [
                [-73.935242, 40.730610],
                [-73.935242, 40.731610]
            ]
        }
    )


class LineaCreate(LineaBase):
    """Schema for creating a new Linea."""
    pass


class LineaUpdate(BaseModel):
    """Schema for updating an existing Linea."""
    
    color: Optional[str] = Field(None, description="Hex color code for the line", max_length=7)
    destino: Optional[str] = Field(None, description="Destination of the line", max_length=255)
    labelLinea: Optional[str] = Field(None, description="Label identifier for the line", max_length=50)
    linea: Optional[int] = Field(None, description="Integer identifier for the line")
    nombreLinea: Optional[str] = Field(None, description="Name of the line", max_length=255)
    recorrido: Optional[dict] = Field(None, description="Geographic LineString geometry representing the route")


class LineaResponse(LineaBase):
    """Schema for Linea response."""
    
    id: int = Field(..., description="Primary key identifier")
    
    @field_validator('recorrido', mode='before')
    @classmethod
    def validate_recorrido(cls, v: Any) -> dict:
        """Convert WKBElement to GeoJSON before validation."""
        if isinstance(v, dict):
            return v
        # If it's a WKBElement from the database, convert it
        return wkbelement_to_geojson(v)
    
    class Config:
        from_attributes = True
