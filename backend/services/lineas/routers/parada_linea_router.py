"""Router for ParadaLinea CRUD endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.lineas.schemas import ParadaLineaCreate, ParadaLineaUpdate, ParadaLineaResponse
from services.lineas.services import ParadaLineaService

router = APIRouter(prefix="/parada-lineas", tags=["parada-lineas"])
service = ParadaLineaService()


@router.post("", response_model=ParadaLineaResponse, status_code=status.HTTP_201_CREATED)
async def create_parada_linea(parada_linea_in: ParadaLineaCreate, db: AsyncSession = Depends(get_db)):
    """Create a new ParadaLinea relationship (link a stop to a line)."""
    result = await service.create_parada_linea(db, parada_linea_in)
    await db.commit()
    return result


@router.get("", response_model=List[ParadaLineaResponse])
async def list_parada_lineas(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """List all ParadaLinea relationships with pagination."""
    return await service.get_all_parada_lineas(db, skip, limit)


@router.get("/{parada_linea_id}", response_model=ParadaLineaResponse)
async def get_parada_linea(parada_linea_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific ParadaLinea relationship by ID."""
    parada_linea = await service.get_parada_linea(db, parada_linea_id)
    if not parada_linea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ParadaLinea not found")
    return parada_linea


@router.put("/{parada_linea_id}", response_model=ParadaLineaResponse)
async def update_parada_linea(
    parada_linea_id: int, parada_linea_in: ParadaLineaUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a ParadaLinea relationship."""
    parada_linea = await service.update_parada_linea(db, parada_linea_id, parada_linea_in)
    if not parada_linea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ParadaLinea not found")
    await db.commit()
    return parada_linea


@router.delete("/{parada_linea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parada_linea(parada_linea_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a ParadaLinea relationship."""
    success = await service.delete_parada_linea(db, parada_linea_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ParadaLinea not found")
    await db.commit()


@router.get("/by-parada/{parada_id}", response_model=List[ParadaLineaResponse])
async def get_parada_lineas_by_parada(parada_id: int, db: AsyncSession = Depends(get_db)):
    """Get all Lineas for a specific Parada."""
    return await service.get_parada_lineas_by_parada(db, parada_id)


@router.get("/by-linea/{linea_id}", response_model=List[ParadaLineaResponse])
async def get_parada_lineas_by_linea(linea_id: int, db: AsyncSession = Depends(get_db)):
    """Get all Paradas for a specific Linea."""
    return await service.get_parada_lineas_by_linea(db, linea_id)


@router.get(
    "/parada/{parada_id}/linea/{linea_id}", response_model=ParadaLineaResponse
)
async def get_parada_linea_relationship(parada_id: int, linea_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific ParadaLinea relationship between a Parada and Linea."""
    parada_linea = await service.get_parada_linea_relationship(db, parada_id, linea_id)
    if not parada_linea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ParadaLinea relationship not found")
    return parada_linea
