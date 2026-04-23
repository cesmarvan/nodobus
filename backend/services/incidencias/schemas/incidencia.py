"""Pydantic schemas for Incidencia model."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any


class IncidenciaBase(BaseModel):
    """Base schema for Incidencia with common fields."""
    
    titulo: str = Field(..., description="Title of the incident")
    descripcion: str = Field(..., description="Detailed description of the incident")
    linea_id: int = Field(..., description="Foreign key reference to the Linea")
    parada_id: Optional[int] = Field(None, description="Foreign key reference to the Parada, if applicable")


class IncidenciaCreate(IncidenciaBase):
    """Schema for creating a new Incidencia."""
    pass


class IncidenciaUpdate(BaseModel):
    """Schema for updating an existing Incidencia."""
    
    parada_id: Optional[int] = Field(None, description="Numerical identifier of the Parada where the incident occurred")
    linea_id: Optional[int] = Field(None, description="Numerical identifier of the Linea associated with the incident")


class IncidenciaResponse(IncidenciaBase):
    """Schema for Incidencia response."""
    
    id: int = Field(..., description="Primary key identifier")
    
    class Config:
        from_attributes = True
