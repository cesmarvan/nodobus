"""Router for Linea CRUD endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.lineas.schemas import LineaCreate, LineaUpdate, LineaResponse
from services.lineas.services import LineaService

router = APIRouter(prefix="/lineas", tags=["lineas"])
service = LineaService()


@router.post("", response_model=LineaResponse, status_code=status.HTTP_201_CREATED)
async def create_linea(linea_in: LineaCreate, db: AsyncSession = Depends(get_db)):
    """Create a new Linea (bus line)."""
    result = await service.create_linea(db, linea_in)
    await db.commit()
    return result


@router.get("", response_model=List[LineaResponse])
async def list_lineas(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """List all Lineas with pagination."""
    return await service.get_all_lineas(db, skip, limit)


@router.get("/{linea_id}", response_model=LineaResponse)
async def get_linea(linea_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific Linea by ID."""
    linea = await service.get_linea(db, linea_id)
    if not linea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Linea not found")
    return linea


@router.put("/{linea_id}", response_model=LineaResponse)
async def update_linea(linea_id: int, linea_in: LineaUpdate, db: AsyncSession = Depends(get_db)):
    """Update a Linea."""
    linea = await service.update_linea(db, linea_id, linea_in)
    if not linea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Linea not found")
    await db.commit()
    return linea


@router.delete("/{linea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_linea(linea_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a Linea."""
    success = await service.delete_linea(db, linea_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Linea not found")
    await db.commit()


@router.get("/by-numero/{linea_numero}", response_model=LineaResponse)
async def get_linea_by_numero(linea_numero: int, db: AsyncSession = Depends(get_db)):
    """Get a Linea by its line number."""
    linea = await service.get_linea_by_numero(db, linea_numero)
    if not linea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Linea not found")
    return linea


@router.get("/search/{nombre}", response_model=List[LineaResponse])
async def search_lineas(nombre: str, db: AsyncSession = Depends(get_db)):
    """Search Lineas by name."""
    return await service.search_lineas_by_nombre(db, nombre)


@router.get("/by-color/{color}", response_model=List[LineaResponse])
async def get_lineas_by_color(color: str, db: AsyncSession = Depends(get_db)):
    """Get all Lineas with a specific color."""
    return await service.get_lineas_by_color(db, color)
