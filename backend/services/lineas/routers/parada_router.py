"""Router for Parada CRUD endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.lineas.schemas import ParadaCreate, ParadaUpdate, ParadaResponse
from services.lineas.services import ParadaService

router = APIRouter(prefix="/api/v1/paradas", tags=["paradas"])
service = ParadaService()


@router.post("", response_model=ParadaResponse, status_code=status.HTTP_201_CREATED)
async def create_parada(parada_in: ParadaCreate, db: AsyncSession = Depends(get_db)):
    """Create a new Parada (stop)."""
    result = await service.create_parada(db, parada_in)
    await db.commit()
    return result


@router.get("", response_model=List[ParadaResponse])
async def list_paradas(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """List all Paradas with pagination."""
    return await service.get_all_paradas(db, skip, limit)


@router.get("/{parada_id}", response_model=ParadaResponse)
async def get_parada(parada_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific Parada by ID."""
    parada = await service.get_parada(db, parada_id)
    if not parada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parada not found")
    return parada


@router.put("/{parada_id}", response_model=ParadaResponse)
async def update_parada(parada_id: int, parada_in: ParadaUpdate, db: AsyncSession = Depends(get_db)):
    """Update a Parada."""
    parada = await service.update_parada(db, parada_id, parada_in)
    if not parada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parada not found")
    await db.commit()
    return parada


@router.delete("/{parada_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parada(parada_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a Parada."""
    success = await service.delete_parada(db, parada_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parada not found")
    await db.commit()


@router.get("/by-nodo/{nodo}", response_model=ParadaResponse)
async def get_parada_by_nodo(nodo: int, db: AsyncSession = Depends(get_db)):
    """Get a Parada by its nodo value."""
    parada = await service.get_parada_by_nodo(db, nodo)
    if not parada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parada not found")
    return parada


@router.get("/search/{nombre}", response_model=List[ParadaResponse])
async def search_paradas(nombre: str, db: AsyncSession = Depends(get_db)):
    """Search Paradas by name."""
    return await service.search_paradas_by_nombre(db, nombre)
