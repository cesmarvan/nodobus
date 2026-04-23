"""Router for Incidencia CRUD endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.incidencias.schemas.incidencia import IncidenciaCreate, IncidenciaUpdate, IncidenciaResponse
from services.incidencias.services.incidencia import IncidenciaService

router = APIRouter(prefix="/api/v1/incidencias", tags=["incidencias"])
service = IncidenciaService()


@router.post("", response_model=IncidenciaResponse, status_code=status.HTTP_201_CREATED)
async def create_incidencia(incidencia_in: IncidenciaCreate, db: AsyncSession = Depends(get_db)):
    """Create a new Incidencia."""
    result = await service.create_incidencia(db, incidencia_in)
    await db.commit()
    return result


@router.get("", response_model=List[IncidenciaResponse])
async def list_incidencias(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """List all Incidencias with pagination."""
    return await service.get_all_incidencias(db, skip, limit)


@router.get("/{incidencia_id}", response_model=IncidenciaResponse)
async def get_incidencia(incidencia_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific Incidencia by ID."""
    incidencia = await service.get_incidencia(db, incidencia_id)
    if not incidencia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incidencia not found")
    return incidencia

@router.get("/linea/{linea_id}", response_model=List[IncidenciaResponse])
async def get_incidencias_by_linea(linea_id: int, db: AsyncSession = Depends(get_db)):
    """Get all Incidencias for a specific Linea."""
    return await service.get_incidencias_by_linea_id(db, linea_id)

@router.get("/parada/{parada_id}", response_model=List[IncidenciaResponse])
async def get_incidencias_by_parada(parada_id: int, db: AsyncSession = Depends(get_db)):
    """Get all Incidencias for a specific Parada."""
    return await service.get_incidencias_by_parada_id(db, parada_id)

@router.put("/{incidencia_id}", response_model=IncidenciaResponse)
async def update_incidencia(incidencia_id: int, incidencia_in: IncidenciaUpdate, db: AsyncSession = Depends(get_db)):
    """Update an Incidencia."""
    incidencia = await service.update_incidencia(db, incidencia_id, incidencia_in)
    if not incidencia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incidencia not found")
    await db.commit()
    return incidencia


@router.delete("/{incidencia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incidencia(incidencia_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an Incidencia."""
    success = await service.delete_incidencia(db, incidencia_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incidencia not found")
    await db.commit()
