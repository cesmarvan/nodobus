"""Sync service for persisting fetched data to database."""

import logging
from datetime import datetime
from typing import Optional

import httpx

from services.fetcher.schemas.common import ErrorDetail, FetchResultResponse
from services.fetcher.services.fetcher_service import FetcherService
from services.fetcher.services.lineas_client import LineasAPIClient
from services.lineas.schemas.autobus import AutobusCreate, AutobusUpdate
from services.lineas.schemas.linea import LineaCreate, LineaUpdate
from services.lineas.schemas.parada import ParadaCreate, ParadaUpdate

logger = logging.getLogger(__name__)


class SyncService:
    """Service for synchronizing fetched data with database.

    This service fetches data from external APIs (ArcGIS, TUSSAM) and syncs it
    to the database using the Lineas service's HTTP API endpoints to maintain
    proper service isolation and loose coupling.
    """

    def __init__(self):
        """Initialize sync service."""
        self.fetcher = FetcherService()
        self.lineas_client = LineasAPIClient()

    async def sync_lineas(self) -> FetchResultResponse:
        """Sync líneas from ArcGIS to database via Lineas service API.

        Returns:
            FetchResultResponse with sync statistics
        """
        start_time = datetime.now()
        created = 0
        updated = 0
        failed = 0
        errors: list[ErrorDetail] = []

        try:
            # Fetch from external ArcGIS API
            fetched_lineas = await self.fetcher.fetch_lineas()

            for linea_data in fetched_lineas:
                try:
                    # Check if línea exists via Lineas service API
                    existing_linea = await self.lineas_client.get_linea_by_numero(
                        linea_data.linea,
                    )

                    if existing_linea:
                        # Update existing via Lineas service API
                        update_data = LineaUpdate(
                            linea=linea_data.linea,
                            nombreLinea=linea_data.nombreLinea,
                            labelLinea=linea_data.labelLinea,
                            destino=linea_data.destino,
                            color=linea_data.color,
                            recorrido=linea_data.recorrido,
                        )
                        await self.lineas_client.update_linea(existing_linea.id, update_data)
                        updated += 1
                        logger.debug(f"Updated línea {linea_data.linea}")
                    else:
                        # Create new via Lineas service API
                        create_data = LineaCreate(
                            linea=linea_data.linea,
                            nombreLinea=linea_data.nombreLinea,
                            labelLinea=linea_data.labelLinea or f"L{linea_data.linea}",
                            destino=linea_data.destino or "",
                            color=linea_data.color or "#000000",
                            recorrido=linea_data.recorrido or {"type": "LineString", "coordinates": []},
                        )
                        await self.lineas_client.create_linea(create_data)
                        created += 1
                        logger.debug(f"Created línea {linea_data.linea}")

                except httpx.HTTPError as e:
                    failed += 1
                    error_msg = f"Failed to sync línea {linea_data.linea}: API error - {e}"
                    logger.error(error_msg, exc_info=True)
                    errors.append(
                        ErrorDetail(
                            code="LINEA_SYNC_ERROR",
                            message=error_msg,
                        ),
                    )
                except Exception as e:
                    failed += 1
                    error_msg = f"Failed to sync línea {linea_data.linea}: {e}"
                    logger.error(error_msg, exc_info=True)
                    errors.append(
                        ErrorDetail(
                            code="LINEA_SYNC_ERROR",
                            message=error_msg,
                        ),
                    )

        except Exception as e:
            logger.error(f"Error in sync_lineas: {e}")
            errors.append(
                ErrorDetail(
                    code="LINEA_FETCH_ERROR",
                    message=f"Failed to fetch líneas: {e}",
                ),
            )

        duration = (datetime.now() - start_time).total_seconds()
        status = "success" if failed == 0 else "partial" if created + updated > 0 else "failed"

        return FetchResultResponse(
            status=status,
            count_created=created,
            count_updated=updated,
            count_failed=failed,
            errors=errors,
            timestamp=datetime.now(),
            duration_seconds=duration,
        )

    async def sync_paradas(self) -> FetchResultResponse:
        """Sync paradas from ArcGIS to database via Lineas service API.

        Returns:
            FetchResultResponse with sync statistics
        """
        start_time = datetime.now()
        created = 0
        updated = 0
        failed = 0
        errors: list[ErrorDetail] = []

        try:
            # Fetch from external ArcGIS API
            fetched_paradas = await self.fetcher.fetch_paradas()

            for parada_data in fetched_paradas:
                try:
                    # Check if parada exists via Lineas service API
                    existing_parada = await self.lineas_client.get_parada_by_nodo(
                        parada_data.nodo,
                    )

                    if existing_parada:
                        # Update existing via Lineas service API
                        update_data = ParadaUpdate(
                            nodo=parada_data.nodo,
                            nombre=parada_data.nombre,
                            localizacion=parada_data.localizacion,
                        )
                        await self.lineas_client.update_parada(existing_parada.id, update_data)
                        updated += 1
                        logger.debug(f"Updated parada {parada_data.nodo}")
                    else:
                        # Create new via Lineas service API
                        create_data = ParadaCreate(
                            nodo=parada_data.nodo,
                            nombre=parada_data.nombre,
                            localizacion=parada_data.localizacion or {"type": "Point", "coordinates": []},
                        )
                        await self.lineas_client.create_parada(create_data)
                        created += 1
                        logger.debug(f"Created parada {parada_data.nodo}")

                except httpx.HTTPError as e:
                    failed += 1
                    error_msg = f"Failed to sync parada {parada_data.nodo}: API error - {e}"
                    logger.error(error_msg, exc_info=True)
                    errors.append(
                        ErrorDetail(
                            code="PARADA_SYNC_ERROR",
                            message=error_msg,
                        ),
                    )
                except Exception as e:
                    failed += 1
                    error_msg = f"Failed to sync parada {parada_data.nodo}: {e}"
                    logger.error(error_msg, exc_info=True)
                    errors.append(
                        ErrorDetail(
                            code="PARADA_SYNC_ERROR",
                            message=error_msg,
                        ),
                    )

        except Exception as e:
            logger.error(f"Error in sync_paradas: {e}")
            errors.append(
                ErrorDetail(
                    code="PARADA_FETCH_ERROR",
                    message=f"Failed to fetch paradas: {e}",
                ),
            )

        duration = (datetime.now() - start_time).total_seconds()
        status = "success" if failed == 0 else "partial" if created + updated > 0 else "failed"

        return FetchResultResponse(
            status=status,
            count_created=created,
            count_updated=updated,
            count_failed=failed,
            errors=errors,
            timestamp=datetime.now(),
            duration_seconds=duration,
        )

    async def sync_autobuses(
        self,
        linea_numero: Optional[int] = None,
    ) -> FetchResultResponse:
        """Sync autobuses from TUSSAM infotus to database via Lineas service API.

        Args:
            linea_numero: Optional línea number to filter by

        Returns:
            FetchResultResponse with sync statistics
        """
        start_time = datetime.now()
        created = 0
        updated = 0
        failed = 0
        errors: list[ErrorDetail] = []

        try:
            # Fetch from external TUSSAM API
            fetched_autobuses = await self.fetcher.fetch_autobuses(linea_numero)

            for autobus_data in fetched_autobuses:
                try:
                    # Check if autobus exists by vehiculo number via Lineas service API
                    existing_autobus = await self.lineas_client.get_autobus_by_vehiculo(
                        autobus_data.vehiculo,
                    )

                    if existing_autobus:
                        # Update existing via Lineas service API
                        update_data = AutobusUpdate(
                            posicion=autobus_data.posicion,
                            sentido=autobus_data.sentido,
                            linea_id=autobus_data.linea,
                        )
                        await self.lineas_client.update_autobus(existing_autobus.id, update_data)
                        updated += 1
                        logger.debug(f"Updated autobus {autobus_data.vehiculo}")
                    else:
                        # Create new via Lineas service API
                        create_data = AutobusCreate(
                            vehiculo=autobus_data.vehiculo,
                            posicion=autobus_data.posicion,
                            sentido=autobus_data.sentido,
                            linea_id=autobus_data.linea,
                        )
                        await self.lineas_client.create_autobus(create_data)
                        created += 1
                        logger.debug(f"Created autobus {autobus_data.vehiculo}")

                except httpx.HTTPError as e:
                    failed += 1
                    error_msg = f"Failed to sync autobus {autobus_data.vehiculo}: API error - {e}"
                    logger.warning(error_msg)
                    errors.append(
                        ErrorDetail(
                            code="AUTOBUS_SYNC_ERROR",
                            message=error_msg,
                        ),
                    )
                except Exception as e:
                    failed += 1
                    error_msg = f"Failed to sync autobus {autobus_data.vehiculo}: {e}"
                    logger.warning(error_msg)
                    errors.append(
                        ErrorDetail(
                            code="AUTOBUS_SYNC_ERROR",
                            message=error_msg,
                        ),
                    )

        except Exception as e:
            logger.error(f"Error in sync_autobuses: {e}")
            errors.append(
                ErrorDetail(
                    code="AUTOBUS_FETCH_ERROR",
                    message=f"Failed to fetch autobuses: {e}",
                ),
            )

        duration = (datetime.now() - start_time).total_seconds()
        status = "success" if failed == 0 else "partial" if created + updated > 0 else "failed"

        return FetchResultResponse(
            status=status,
            count_created=created,
            count_updated=updated,
            count_failed=failed,
            errors=errors,
            timestamp=datetime.utcnow(),
            duration_seconds=duration,
        )
