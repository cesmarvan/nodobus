"""Router for Autobus CRUD endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.lineas.schemas import AutobusCreate, AutobusUpdate, AutobusResponse
from services.lineas.services import AutobusService

router = APIRouter(prefix="/autobuses", tags=["autobuses"])
service = AutobusService()


@router.post("", response_model=AutobusResponse, status_code=status.HTTP_201_CREATED)
async def create_autobus(autobus_in: AutobusCreate, db: AsyncSession = Depends(get_db)):
    """Create a new Autobus (bus)."""
    result = await service.create_autobus(db, autobus_in)
    await db.commit()
    return result


@router.get("", response_model=List[AutobusResponse])
async def list_autobuses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """List all Autobuses with pagination."""
    return await service.get_all_autobuses(db, skip, limit)


@router.get("/{autobus_id}", response_model=AutobusResponse)
async def get_autobus(autobus_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific Autobus by ID."""
    autobus = await service.get_autobus(db, autobus_id)
    if not autobus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autobus not found")
    return autobus


@router.put("/{autobus_id}", response_model=AutobusResponse)
async def update_autobus(autobus_id: int, autobus_in: AutobusUpdate, db: AsyncSession = Depends(get_db)):
    """Update an Autobus."""
    autobus = await service.update_autobus(db, autobus_id, autobus_in)
    if not autobus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autobus not found")
    await db.commit()
    return autobus


@router.delete("/{autobus_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_autobus(autobus_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an Autobus."""
    success = await service.delete_autobus(db, autobus_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autobus not found")
    await db.commit()


@router.get("/by-vehiculo/{vehiculo}", response_model=AutobusResponse)
async def get_autobus_by_vehiculo(vehiculo: int, db: AsyncSession = Depends(get_db)):
    """Get an Autobus by its vehicle identifier."""
    autobus = await service.get_autobus_by_vehiculo(db, vehiculo)
    if not autobus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autobus not found")
    return autobus


@router.get("/by-linea/{linea_id}", response_model=List[AutobusResponse])
async def get_autobuses_by_linea(linea_id: int, db: AsyncSession = Depends(get_db)):
    """Get all Autobuses for a specific Linea."""
    return await service.get_autobuses_by_linea(db, linea_id)


@router.get("/by-sentido/{sentido}", response_model=List[AutobusResponse])
async def get_autobuses_by_sentido(sentido: int, db: AsyncSession = Depends(get_db)):
    """Get all Autobuses with a specific direction."""
    return await service.get_autobuses_by_sentido(db, sentido)
