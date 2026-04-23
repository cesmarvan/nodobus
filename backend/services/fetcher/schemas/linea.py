"""Schemas for ArcGIS FeatureServer responses - Líneas."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class ArcGISGeometry(BaseModel):
    """ArcGIS geometry object (Point or LineString)."""

    x: Optional[float] = None
    y: Optional[float] = None
    paths: Optional[list[list[list[float]]]] = None  # For LineString
    spatialReference: Optional[dict[str, Any]] = None


class ArcGISAttributes(BaseModel):
    """ArcGIS feature attributes for línea."""

    OBJECTID: Optional[int] = Field(None, alias="ObjectId")
    LINEA: Optional[int] = Field(None, alias="Linea")  # Line number
    NOMBRE: Optional[str] = Field(None, alias="NombreLinea")  # API returns "NombreLinea"
    LABEL_LINEA: Optional[str] = Field(None, alias="LabelLinea")  # API returns "LabelLinea"
    COLOR: Optional[str] = Field(None, alias="Color")  # API returns "Color"
    DESTINO: Optional[str] = Field(None, alias="DestinoRuta")  # API returns "DestinoRuta" (destination)
    
    model_config = {"extra": "allow", "populate_by_name": True}  # Allow extra fields and both alias and field name


class ArcGISFeature(BaseModel):
    """Single feature from ArcGIS FeatureServer."""

    geometry: ArcGISGeometry
    attributes: ArcGISAttributes


class ArcGISLineaResponse(BaseModel):
    """ArcGIS FeatureServer response for líneas query."""

    features: list[ArcGISFeature]
    exceededTransferLimit: bool = False


class LineaFetchSchema(BaseModel):
    """Internal schema for línea after transformation."""

    linea: int  # Matches LineaCreate.linea
    nombreLinea: str  # Matches LineaCreate.nombreLinea
    labelLinea: Optional[str] = None  # Matches LineaCreate.labelLinea
    destino: Optional[str] = None  # Matches LineaCreate.destino
    color: Optional[str] = None  # Matches LineaCreate.color
    recorrido: Optional[dict[str, Any]] = None  # Matches LineaCreate.recorrido (GeoJSON LineString)

    class Config:
        from_attributes = True
