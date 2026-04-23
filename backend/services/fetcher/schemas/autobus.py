"""Schemas for TUSSAM infotus API responses - Autobuses."""

from typing import Any, Optional

from pydantic import BaseModel


class TussamAutobusData(BaseModel):
    """TUSSAM infotus API response data for a bus."""

    vehiculo: int = None  # Bus number/ID - may not always be present
    linea: int = None  # Line number - may not always be present
    sentido: int = None  # Direction (0 or 1) - may not always be present
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    # Add other fields as needed based on actual API response

    model_config = {"extra": "allow"}


class AutobusFetchSchema(BaseModel):
    """Internal schema for autobus after transformation."""

    vehiculo: int
    linea: int
    sentido: int
    posicion: Optional[dict[str, Any]] = None  # GeoJSON Point

    model_config = {"from_attributes": True}
