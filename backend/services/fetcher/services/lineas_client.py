"""HTTP client for accessing Lineas service API."""

import logging
from typing import Optional

import httpx

from core.config import get_settings
from services.lineas.schemas.linea import LineaCreate, LineaResponse, LineaUpdate
from services.lineas.schemas.parada import ParadaCreate, ParadaResponse, ParadaUpdate
from services.lineas.schemas.parada_linea import ParadaLineaCreate, ParadaLineaResponse

logger = logging.getLogger(__name__)
settings = get_settings()


class LineasAPIClient:
    """HTTP client for Lineas service API."""

    def __init__(self, timeout: int = 30):
        """Initialize lineas API client.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.base_url = settings.lineas_service_base_url
        self.timeout = timeout

    async def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[dict] = None,
    ) -> dict:
        """Make HTTP request to lineas service.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., /lineas, /paradas/1)
            json_data: JSON payload for POST/PUT requests

        Returns:
            JSON response

        Raises:
            httpx.HTTPError: If request fails
        """
        url = f"{self.base_url}{settings.api_prefix}{endpoint}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(method, url, json=json_data)
                response.raise_for_status()
                
                if response.status_code == 204:
                    # No content response
                    return {}
                
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"API request failed: {method} {url} - {e.response.status_code}")
                logger.error(f"Response: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error making request to {url}: {e}")
                raise

    # Linea operations
    
    async def get_linea_by_numero(self, linea_numero: int) -> Optional[LineaResponse]:
        """Get a Linea by its line number.

        Args:
            linea_numero: Line number

        Returns:
            LineaResponse or None if not found
        """
        try:
            data = await self._request("GET", f"/lineas/by-numero/{linea_numero}")
            return LineaResponse(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(f"Error getting linea by numero {linea_numero}: {e}")
            return None

    async def create_linea(self, linea_data: LineaCreate) -> LineaResponse:
        """Create a new Linea.

        Args:
            linea_data: LineaCreate schema

        Returns:
            Created LineaResponse
        """
        data = await self._request("POST", "/lineas", linea_data.model_dump())
        return LineaResponse(**data)

    async def update_linea(self, linea_id: int, linea_data: LineaUpdate) -> Optional[LineaResponse]:
        """Update a Linea.

        Args:
            linea_id: Linea ID
            linea_data: LineaUpdate schema

        Returns:
            Updated LineaResponse or None if not found
        """
        try:
            data = await self._request("PUT", f"/lineas/{linea_id}", linea_data.model_dump(exclude_unset=True))
            return LineaResponse(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"Linea {linea_id} not found")
                return None
            raise
        except Exception as e:
            logger.error(f"Error updating linea {linea_id}: {e}")
            raise

    async def get_linea_by_labelLinea(self, labelLinea: str) -> Optional[LineaResponse]:
        """Get a Linea by its label identifier.

        Args:
            labelLinea: Line label identifier

        Returns:
            LineaResponse or None if not found
        """
        try:
            data = await self._request("GET", f"/lineas/by-label/{labelLinea}")
            return LineaResponse(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(f"Error getting linea by labelLinea {labelLinea}: {e}")
            return None

    # Parada operations

    async def get_parada_by_nodo(self, nodo: int) -> Optional[ParadaResponse]:
        """Get a Parada by its nodo value.

        Args:
            nodo: Parada nodo value

        Returns:
            ParadaResponse or None if not found
        """
        try:
            data = await self._request("GET", f"/paradas/by-nodo/{nodo}")
            return ParadaResponse(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(f"Error getting parada by nodo {nodo}: {e}")
            return None

    async def create_parada(self, parada_data: ParadaCreate) -> ParadaResponse:
        """Create a new Parada.

        Args:
            parada_data: ParadaCreate schema

        Returns:
            Created ParadaResponse
        """
        data = await self._request("POST", "/paradas", parada_data.model_dump())
        return ParadaResponse(**data)

    async def update_parada(self, parada_id: int, parada_data: ParadaUpdate) -> Optional[ParadaResponse]:
        """Update a Parada.

        Args:
            parada_id: Parada ID
            parada_data: ParadaUpdate schema

        Returns:
            Updated ParadaResponse or None if not found
        """
        try:
            data = await self._request("PUT", f"/paradas/{parada_id}", parada_data.model_dump(exclude_unset=True))
            return ParadaResponse(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"Parada {parada_id} not found")
                return None
            raise
        except Exception as e:
            logger.error(f"Error updating parada {parada_id}: {e}")
            raise

    # ParadaLinea operations

    async def get_parada_linea_relationship(
        self, parada_id: int, linea_id: int
    ) -> Optional[ParadaLineaResponse]:
        """Get a specific ParadaLinea relationship between a Parada and Linea.

        Args:
            parada_id: Parada ID
            linea_id: Linea ID

        Returns:
            ParadaLineaResponse or None if not found
        """
        try:
            data = await self._request("GET", f"/parada-lineas/parada/{parada_id}/linea/{linea_id}")
            return ParadaLineaResponse(**data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(
                f"Error getting parada_linea relationship for parada {parada_id}, "
                f"linea {linea_id}: {e}"
            )
            return None

    async def create_parada_linea(self, parada_linea_data: ParadaLineaCreate) -> ParadaLineaResponse:
        """Create a new ParadaLinea relationship.

        Args:
            parada_linea_data: ParadaLineaCreate schema

        Returns:
            Created ParadaLineaResponse
        """
        data = await self._request("POST", "/parada-lineas", parada_linea_data.model_dump())
        return ParadaLineaResponse(**data)
    
