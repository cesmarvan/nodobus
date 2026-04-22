"""Schemas for the Lineas service."""

from .parada import ParadaCreate, ParadaUpdate, ParadaResponse
from .linea import LineaCreate, LineaUpdate, LineaResponse
from .autobus import AutobusCreate, AutobusUpdate, AutobusResponse
from .parada_linea import ParadaLineaCreate, ParadaLineaUpdate, ParadaLineaResponse

__all__ = [
    "ParadaCreate",
    "ParadaUpdate",
    "ParadaResponse",
    "LineaCreate",
    "LineaUpdate",
    "LineaResponse",
    "AutobusCreate",
    "AutobusUpdate",
    "AutobusResponse",
    "ParadaLineaCreate",
    "ParadaLineaUpdate",
    "ParadaLineaResponse",
]
