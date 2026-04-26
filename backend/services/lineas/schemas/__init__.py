"""Schemas for the Lineas service."""

from .parada import ParadaCreate, ParadaUpdate, ParadaResponse
from .linea import LineaCreate, LineaUpdate, LineaResponse
from .parada_linea import ParadaLineaCreate, ParadaLineaUpdate, ParadaLineaResponse

__all__ = [
    "ParadaCreate",
    "ParadaUpdate",
    "ParadaResponse",
    "LineaCreate",
    "LineaUpdate",
    "LineaResponse",
    "ParadaLineaCreate",
    "ParadaLineaUpdate",
    "ParadaLineaResponse",
]
