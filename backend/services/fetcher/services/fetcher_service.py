"""Fetcher service for retrieving data from external APIs."""

import json
import logging
from typing import Optional

import httpx


from services.fetcher.exceptions import ExternalAPIError, ValidationError
from services.fetcher.schemas.autobus import (
    AutobusFetchSchema,
    TussamAutobusData,
)
from services.fetcher.schemas.linea import (
    ArcGISLineaResponse,
    LineaFetchSchema,
)
from services.fetcher.schemas.parada import (
    ArcGISParadaResponse,
    ParadaFetchSchema,
)
from services.fetcher.services.retry_handler import (
    RetryConfig,
    retry_with_backoff,
)
from core.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)



class FetcherService:
    """Service for fetching data from external APIs."""

    def __init__(self, timeout: int = 30):
        """Initialize fetcher service.

        Args:
            timeout: HTTP request timeout in seconds
        """
        self.timeout = timeout
        self.retry_config = RetryConfig(
            base_delay=1.0,
            max_retries=3,
            max_delay=60.0,
        )

    @retry_with_backoff(config=RetryConfig())
    async def _fetch_url(self, url: str) -> dict:
        """Fetch JSON from URL with retry logic.

        Args:
            url: URL to fetch

        Returns:
            Parsed JSON response

        Raises:
            ExternalAPIError: If fetch fails after retries
            ValidationError: If response is invalid
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()

            try:
                data = response.json()
                logger.debug(f"Raw API response (first 2000 chars): {str(data)[:2000]}")
                if isinstance(data, dict) and "features" in data:
                    logger.debug(f"Response has {len(data.get('features', []))} features")
                    if data.get('features'):
                        logger.debug(f"First feature attributes: {data['features'][0].get('attributes', {})}")
                return data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from {url}: {e}")
                logger.error(f"Response text: {response.text[:500]}")
                raise ValidationError(f"Invalid JSON response from {url}") from e

    async def fetch_lineas(self) -> list[LineaFetchSchema]:
        """Fetch líneas from ArcGIS FeatureServer.

        Returns:
            List of formatted línea objects

        Raises:
            ExternalAPIError: If fetch fails
            ValidationError: If response is invalid
        """
        logger.info("Fetching líneas from ArcGIS...")

        try:
            data = await self._fetch_url(settings.tussam_arcgis_lineas_url)
            
            # Check for error in response
            if "error" in data:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                logger.error(f"ArcGIS API error: {error_msg}")
                raise ExternalAPIError(f"ArcGIS API error: {error_msg}")
            
            response = ArcGISLineaResponse(**data)
            
            logger.info(f"Received {len(response.features)} features from ArcGIS")
            if response.features:
                # Log the first feature's attributes for debugging
                first_feature = response.features[0]
                logger.debug(f"First feature attributes: {first_feature.attributes.model_dump()}")

            lineas = []
            for idx, feature in enumerate(response.features):
                try:
                    # Skip features with missing required fields
                    if feature.attributes.LINEA is None or feature.attributes.NOMBRE is None:
                        logger.warning(
                            f"Feature {idx}: Skipping línea with missing required fields - "
                            f"LINEA={feature.attributes.LINEA}, NOMBRE={feature.attributes.NOMBRE}, "
                            f"All attributes: {feature.attributes.model_dump()}"
                        )
                        continue
                    
                    # Transform geometry to GeoJSON LineString
                    recorrido = None
                    if feature.geometry.paths:
                        recorrido = {
                            "type": "LineString",
                            "coordinates": [
                                [coord[0], coord[1]]
                                for path in feature.geometry.paths
                                for coord in path
                            ],
                        }

                    linea = LineaFetchSchema(
                        linea=feature.attributes.LINEA,
                        nombreLinea=feature.attributes.NOMBRE,
                        labelLinea=feature.attributes.LABEL_LINEA,
                        destino=feature.attributes.DESTINO,
                        color=feature.attributes.COLOR,
                        recorrido=recorrido,
                    )
                    lineas.append(linea)
                except Exception as e:
                    linea_numero = getattr(feature.attributes, "LINEA", "unknown")
                    logger.error(
                        f"Failed to transform línea feature {linea_numero}: {e}",
                        exc_info=True
                    )

            logger.info(f"Successfully fetched {len(lineas)} válid líneas (from {len(response.features)} total features)")
            return lineas

        except ValidationError:
            raise
        except ExternalAPIError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching líneas: {e}")
            raise ExternalAPIError(f"Failed to fetch líneas: {e}") from e

    async def fetch_paradas(self) -> list[ParadaFetchSchema]:
        """Fetch paradas from ArcGIS FeatureServer.

        Returns:
            List of formatted parada objects

        Raises:
            ExternalAPIError: If fetch fails
            ValidationError: If response is invalid
        """
        logger.info("Fetching paradas from ArcGIS...")

        try:
            data = await self._fetch_url(settings.tussam_arcgis_paradas_url)
            
            # Check for error in response
            if "error" in data:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                logger.error(f"ArcGIS API error: {error_msg}")
                raise ExternalAPIError(f"ArcGIS API error: {error_msg}")
            
            response = ArcGISParadaResponse(**data)

            paradas = []
            for idx, feature in enumerate(response.features):
                try:
                    # Skip features with missing required fields
                    if feature.attributes.NODO is None or feature.attributes.NOMBRE is None:
                        logger.warning(
                            f"Feature {idx}: Skipping parada with missing required fields - "
                            f"NODO={feature.attributes.NODO}, NOMBRE={feature.attributes.NOMBRE}"
                        )
                        continue
                    
                    # Transform geometry to GeoJSON Point
                    localizacion = None
                    logger.debug(f"Parada {idx} geometry: x={feature.geometry.x}, y={feature.geometry.y}")
                    if feature.geometry.x is not None and feature.geometry.y is not None:
                        localizacion = {
                            "type": "Point",
                            "coordinates": [feature.geometry.x, feature.geometry.y],
                        }
                        logger.debug(f"Created localizacion: {localizacion}")
                    else:
                        logger.warning(f"Parada {idx} ({feature.attributes.NODO}): Missing geometry coordinates")

                    parada = ParadaFetchSchema(
                        nodo=feature.attributes.NODO,
                        nombre=feature.attributes.NOMBRE,
                        codigo=feature.attributes.CODIGO,
                        descripcion=feature.attributes.DESCRIPCION,
                        labelLinea=feature.attributes.LABELLINEA,
                        localizacion=localizacion,
                    )
                    paradas.append(parada)
                except Exception as e:
                    nodo = getattr(feature.attributes, "NODO", "unknown")
                    logger.warning(
                        f"Failed to transform parada feature {nodo}: {e}",
                    )

            logger.info(f"Successfully fetched {len(paradas)} paradas")
            return paradas

        except ValidationError:
            raise
        except ExternalAPIError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching paradas: {e}")
            raise ExternalAPIError(f"Failed to fetch paradas: {e}") from e

    async def fetch_autobuses(self, linea_numero: Optional[int] = None) -> list[AutobusFetchSchema]:
        """Fetch autobuses from TUSSAM infotus API.

        Args:
            linea_numero: Optional línea number to filter by

        Returns:
            List of formatted autobus objects

        Raises:
            ExternalAPIError: If fetch fails
            ValidationError: If response is invalid
        """
        logger.info(f"Fetching autobuses from TUSSAM infotus (línea: {linea_numero})...")

        try:
            # Build URL with line filter if provided
            url = settings.tussam_infotus_base_url
            if linea_numero:
                url = f"{url}/{linea_numero}"

            data = await self._fetch_url(url)

            # Check for error in response
            if isinstance(data, dict) and "error" in data:
                error_msg = data.get("error", {}).get("message", "Unknown error") if isinstance(data.get("error"), dict) else str(data.get("error"))
                logger.error(f"TUSSAM API error: {error_msg}")
                raise ExternalAPIError(f"TUSSAM API error: {error_msg}")

            # Handle different response formats (array or object)
            autobuses_data = data if isinstance(data, list) else data.get("data", []) if isinstance(data, dict) else []

            autobuses = []
            for bus_data in autobuses_data:
                try:
                    bus = TussamAutobusData(**bus_data)

                    # Transform geometry to GeoJSON Point - only if coordinates exist
                    posicion = None
                    if bus.latitud is not None and bus.longitud is not None:
                        posicion = {
                            "type": "Point",
                            "coordinates": [bus.longitud, bus.latitud],
                        }

                    # Only add autobus if required fields are present
                    if bus.vehiculo is not None and bus.linea is not None:
                        autobus = AutobusFetchSchema(
                            vehiculo=bus.vehiculo,
                            linea=bus.linea,
                            sentido=bus.sentido or 0,
                            posicion=posicion,
                        )
                        autobuses.append(autobus)
                except Exception as e:
                    logger.warning(f"Failed to transform autobus feature: {bus_data}: {e}")

            logger.info(f"Successfully fetched {len(autobuses)} autobuses")
            return autobuses

        except ValidationError:
            raise
        except ExternalAPIError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching autobuses: {e}")
            raise ExternalAPIError(f"Failed to fetch autobuses: {e}") from e
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching autobuses: {e}")
            raise ExternalAPIError(f"Failed to fetch autobuses: {e}") from e
