"""Schemas for ArcGIS FeatureServer responses - Paradas."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class ArcGISParadaGeometry(BaseModel):
    """ArcGIS Point geometry for parada."""

    x: Optional[float] = None
    y: Optional[float] = None
    spatialReference: Optional[dict[str, Any]] = None


class ArcGISParadaAttributes(BaseModel):
    """ArcGIS feature attributes for parada."""

    OBJECTID: Optional[int] = Field(None, alias="ObjectId")
    NODO: Optional[int] = Field(None, alias="Nodo")  # Stop node ID
    NOMBRE: Optional[str] = Field(None, alias="Nombre")
    CODIGO: Optional[str] = Field(None, alias="Codigo")  # Optional field
    DESCRIPCION: Optional[str] = Field(None, alias="Description")  # Optional field
    LABELLINEA: Optional[str] = Field(None, alias="LabelLinea")  # Line label from ArcGIS
    # Add other fields as needed based on actual API response

    model_config = {"extra": "allow", "populate_by_name": True}


class ArcGISParadaFeature(BaseModel):
    """Single parada feature from ArcGIS FeatureServer."""

    geometry: ArcGISParadaGeometry
    attributes: ArcGISParadaAttributes


class ArcGISParadaResponse(BaseModel):
    """ArcGIS FeatureServer response for paradas query."""

    features: list[ArcGISParadaFeature]
    exceededTransferLimit: bool = False


class ParadaFetchSchema(BaseModel):
    """Internal schema for parada after transformation."""

    nodo: int
    nombre: str
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    labelLinea: Optional[str] = None  # Line label from ArcGIS
    localizacion: Optional[dict[str, Any]] = None  # GeoJSON Point

    class Config:
        from_attributes = True
