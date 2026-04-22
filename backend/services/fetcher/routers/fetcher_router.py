"""Router for fetcher service API endpoints."""

import logging

from fastapi import APIRouter
from services.fetcher.schemas.common import FetchResultResponse
from services.fetcher.services.sync_service import SyncService
from services.fetcher.tasks import (
    sync_autobuses_task,
    sync_lineas_task,
    sync_paradas_task,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/fetch",
    tags=["fetcher"],
)


@router.post("/lineas", response_model=FetchResultResponse)
async def fetch_lineas():
    """Trigger fetch and sync of líneas from ArcGIS.

    **Endpoints called:**
    - TUSSAM ArcGIS FeatureServer Líneas endpoint
    - Lineas service API for create/update operations

    **Returns:**
    - count_created: Number of new líneas created
    - count_updated: Number of existing líneas updated
    - count_failed: Number of failed sync operations
    - errors: List of any errors encountered

    This endpoint triggers a background Celery task to fetch líneas from the
    ArcGIS FeatureServer and sync them to the database via the Lineas service API.
    """
    try:
        # Trigger async task
        sync_lineas_task.delay()

        # For now, return from sync service directly (no async/celery)
        sync_service = SyncService()
        result = await sync_service.sync_lineas()
        logger.info(
            f"Sync líneas: created={result.count_created}, "
            f"updated={result.count_updated}, failed={result.count_failed}"
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching líneas: {e}")
        raise


@router.post("/paradas", response_model=FetchResultResponse)
async def fetch_paradas():
    """Trigger fetch and sync of paradas from ArcGIS.

    **Endpoints called:**
    - TUSSAM ArcGIS FeatureServer Paradas endpoint
    - Lineas service API for create/update operations

    **Returns:**
    - count_created: Number of new paradas created
    - count_updated: Number of existing paradas updated
    - count_failed: Number of failed sync operations
    - errors: List of any errors encountered

    This endpoint triggers a background Celery task to fetch paradas from the
    ArcGIS FeatureServer and sync them to the database via the Lineas service API.
    """
    try:
        # Trigger async task
        sync_paradas_task.delay()

        # For now, return from sync service directly (no async/celery)
        sync_service = SyncService()
        result = await sync_service.sync_paradas()
        logger.info(
            f"Sync paradas: created={result.count_created}, "
            f"updated={result.count_updated}, failed={result.count_failed}"
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching paradas: {e}")
        raise


@router.post("/autobuses/{linea_numero}", response_model=FetchResultResponse)
async def fetch_autobuses_by_line(linea_numero: int):
    """Trigger fetch and sync of autobuses for a specific línea from TUSSAM infotus.

    **Path Parameters:**
    - linea_numero: Line number to fetch buses for

    **Endpoints called:**
    - TUSSAM infotus API for the specified línea
    - Lineas service API for create/update operations

    **Returns:**
    - count_created: Number of new autobuses created
    - count_updated: Number of existing autobuses updated
    - count_failed: Number of failed sync operations
    - errors: List of any errors encountered

    This endpoint triggers a background Celery task to fetch autobuses from the
    TUSSAM infotus API for the specified línea and sync them to the database
    via the Lineas service API.
    """
    try:
        # Trigger async task
        sync_autobuses_task.delay(linea_numero)

        # For now, return from sync service directly (no async/celery)
        sync_service = SyncService()
        result = await sync_service.sync_autobuses(linea_numero)
        logger.info(
            f"Sync autobuses (línea {linea_numero}): created={result.count_created}, "
            f"updated={result.count_updated}, failed={result.count_failed}"
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching autobuses for línea {linea_numero}: {e}")
        raise


@router.post("/autobuses", response_model=FetchResultResponse)
async def fetch_all_autobuses():
    """Trigger fetch and sync of all autobuses from TUSSAM infotus.

    **Endpoints called:**
    - TUSSAM infotus API (all buses)
    - Lineas service API for create/update operations

    **Returns:**
    - count_created: Number of new autobuses created
    - count_updated: Number of existing autobuses updated
    - count_failed: Number of failed sync operations
    - errors: List of any errors encountered

    This endpoint triggers a background Celery task to fetch all autobuses from the
    TUSSAM infotus API and sync them to the database via the Lineas service API.
    """
    try:
        # Trigger async task
        sync_autobuses_task.delay()

        # For now, return from sync service directly (no async/celery)
        sync_service = SyncService()
        result = await sync_service.sync_autobuses()
        logger.info(
            f"Sync all autobuses: created={result.count_created}, "
            f"updated={result.count_updated}, failed={result.count_failed}"
        )
        return result
    except Exception as e:
        logger.error(f"Error fetching all autobuses: {e}")
        raise


@router.post("/all", response_model=FetchResultResponse)
async def fetch_all_data():
    """Trigger complete sync of all data (líneas, paradas, autobuses).

    **Endpoints called:**
    - TUSSAM ArcGIS FeatureServer Líneas endpoint
    - TUSSAM ArcGIS FeatureServer Paradas endpoint
    - TUSSAM infotus API (all buses)
    - Lineas service API for create/update operations

    **Returns:**
    - Combined statistics from all three fetches

    This endpoint triggers background Celery tasks to fetch all data from all
    external APIs and sync them to the database via the Lineas service API.
    """
    try:
        # Trigger all async tasks
        sync_lineas_task.delay()
        sync_paradas_task.delay()
        sync_autobuses_task.delay()

        # For now, execute all syncs sequentially
        sync_service = SyncService()

        result_lineas = await sync_service.sync_lineas()
        result_paradas = await sync_service.sync_paradas()
        result_autobuses = await sync_service.sync_autobuses()

        # Combine results
        combined_result = FetchResultResponse(
            status="success"
            if result_lineas.count_failed == 0
            and result_paradas.count_failed == 0
            and result_autobuses.count_failed == 0
            else "partial",
            count_created=(
                result_lineas.count_created
                + result_paradas.count_created
                + result_autobuses.count_created
            ),
            count_updated=(
                result_lineas.count_updated
                + result_paradas.count_updated
                + result_autobuses.count_updated
            ),
            count_failed=(
                result_lineas.count_failed
                + result_paradas.count_failed
                + result_autobuses.count_failed
            ),
            errors=result_lineas.errors + result_paradas.errors + result_autobuses.errors,
            timestamp=result_autobuses.timestamp,
            duration_seconds=(
                result_lineas.duration_seconds
                + result_paradas.duration_seconds
                + result_autobuses.duration_seconds
            ),
        )

        logger.info(
            f"Complete sync: created={combined_result.count_created}, "
            f"updated={combined_result.count_updated}, failed={combined_result.count_failed}"
        )
        return combined_result
    except Exception as e:
        logger.error(f"Error in complete sync: {e}")
        raise
