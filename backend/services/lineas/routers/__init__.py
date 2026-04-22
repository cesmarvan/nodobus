"""Routers for the Lineas module."""

from .parada_router import router as parada_router
from .linea_router import router as linea_router
from .autobus_router import router as autobus_router
from .parada_linea_router import router as parada_linea_router

__all__ = [
    "parada_router",
    "linea_router",
    "autobus_router",
    "parada_linea_router",
]
