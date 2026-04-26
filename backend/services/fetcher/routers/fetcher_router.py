"""Router for fetcher service API endpoints."""

import logging

from fastapi import APIRouter, HTTPException
from services.fetcher.schemas.common import FetchResultResponse
from services.fetcher.services.sync_service import SyncService
from services.fetcher.services.tussam_client import TussamAPIClient

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

    This endpoint fetches líneas from the
    ArcGIS FeatureServer and sync them to the database via the Lineas service API.
    """
    try:
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

    This endpoint fetches paradas from the
    ArcGIS FeatureServer and sync them to the database via the Lineas service API.
    """
    try:
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


@router.get("/tussam/buses/{line_label}")
async def get_real_time_buses(line_label: str):
    """Get real-time buses for a specific line from TUSSAM API.

    Args:
        line_label: Line label/number (e.g., "25", "C3")

    Returns:
        JSON response with real-time bus data from TUSSAM API
    """
    try:
        client = TussamAPIClient()
        data = await client.get_buses_by_line(line_label)
        logger.info(f"Successfully fetched buses for line {line_label}")
        return data
    except Exception as e:
        logger.error(f"Error fetching real-time buses for line {line_label}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch real-time buses: {str(e)}")






