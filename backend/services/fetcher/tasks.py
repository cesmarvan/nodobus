"""Celery tasks for fetcher service."""

import logging
from typing import Optional

from services.fetcher.celery_app import app
from services.fetcher.services.sync_service import SyncService

logger = logging.getLogger(__name__)


@app.task(bind=True)
def sync_lineas_task(self):
    """Task to sync líneas from ArcGIS to database.

    Returns:
        Dict with sync result statistics
    """
    import asyncio

    try:
        result = asyncio.run(_sync_lineas_async())
        return {
            "status": result.status,
            "created": result.count_created,
            "updated": result.count_updated,
            "failed": result.count_failed,
            "errors": [e.dict() for e in result.errors],
        }
    except Exception as e:
        logger.error(f"Error in sync_lineas_task: {e}")
        raise


@app.task(bind=True)
def sync_paradas_task(self):
    """Task to sync paradas from ArcGIS to database.

    Returns:
        Dict with sync result statistics
    """
    import asyncio

    try:
        result = asyncio.run(_sync_paradas_async())
        return {
            "status": result.status,
            "created": result.count_created,
            "updated": result.count_updated,
            "failed": result.count_failed,
            "errors": [e.dict() for e in result.errors],
        }
    except Exception as e:
        logger.error(f"Error in sync_paradas_task: {e}")
        raise


@app.task(bind=True)
def sync_autobuses_task(self, linea_numero: Optional[int] = None):
    """Task to sync autobuses from TUSSAM infotus to database.

    Args:
        linea_numero: Optional línea number to filter by

    Returns:
        Dict with sync result statistics
    """
    import asyncio

    try:
        result = asyncio.run(_sync_autobuses_async(linea_numero))
        return {
            "status": result.status,
            "created": result.count_created,
            "updated": result.count_updated,
            "failed": result.count_failed,
            "errors": [e.dict() for e in result.errors],
        }
    except Exception as e:
        logger.error(f"Error in sync_autobuses_task: {e}")
        raise


async def _sync_lineas_async():
    """Helper to sync líneas asynchronously."""
    sync_service = SyncService()
    return await sync_service.sync_lineas()


async def _sync_paradas_async():
    """Helper to sync paradas asynchronously."""
    sync_service = SyncService()
    return await sync_service.sync_paradas()


async def _sync_autobuses_async(linea_numero: Optional[int] = None):
    """Helper to sync autobuses asynchronously."""
    sync_service = SyncService()
    return await sync_service.sync_autobuses(linea_numero)
