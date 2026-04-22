"""Pydantic schemas for ParadaLinea model."""

from pydantic import BaseModel, Field
from typing import Optional


class ParadaLineaBase(BaseModel):
    """Base schema for ParadaLinea with common fields."""
    
    parada_id: int = Field(..., description="Foreign key referencing Parada")
    linea_id: int = Field(..., description="Foreign key referencing Linea")


class ParadaLineaCreate(ParadaLineaBase):
    """Schema for creating a new ParadaLinea."""
    pass


class ParadaLineaUpdate(BaseModel):
    """Schema for updating an existing ParadaLinea."""
    
    parada_id: Optional[int] = Field(None, description="Foreign key referencing Parada")
    linea_id: Optional[int] = Field(None, description="Foreign key referencing Linea")


class ParadaLineaResponse(ParadaLineaBase):
    """Schema for ParadaLinea response."""
    
    id: int = Field(..., description="Primary key identifier")
    
    class Config:
        from_attributes = True
