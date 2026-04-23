"""Service layer for Incidencia CRUD operations."""

from typing import List, Optional
from services.incidencias.repositories.incidencia import IncidenciaRepository
from services.incidencias.schemas.incidencia import IncidenciaCreate, IncidenciaResponse, IncidenciaUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class IncidenciaService:
    """Service for Incidencia operations."""
    
    def __init__(self):
        self.repository = IncidenciaRepository()
    
    async def create_incidencia(self, db: AsyncSession, incidencia_in: IncidenciaCreate) -> IncidenciaResponse:
        """Create a new Incidencia."""
        db_incidencia = await self.repository.create(db, incidencia_in)
        return IncidenciaResponse.model_validate(db_incidencia)
    
    async def get_incidencia(self, db: AsyncSession, incidencia_id: int) -> Optional[IncidenciaResponse]:
        """Retrieve an Incidencia by ID."""
        db_incidencia = await self.repository.get(db, incidencia_id)
        if db_incidencia:
            return IncidenciaResponse.model_validate(db_incidencia)
        return None
    
    async def get_all_incidencias(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[IncidenciaResponse]:
        """Retrieve all Incidencias."""
        db_incidencias = await self.repository.get_all(db, skip, limit)
        return [IncidenciaResponse.model_validate(i) for i in db_incidencias]
    
    async def get_incidencias_by_parada_id(self, db: AsyncSession, parada_id: int, skip: int = 0, limit: int = 100) -> List[IncidenciaResponse]:
        """Retrieve all Incidencias for a specific Parada."""
        db_incidencias = await self.repository.get_by_parada_id(db, parada_id)
        return [IncidenciaResponse.model_validate(i) for i in db_incidencias]
    
    async def get_incidencias_by_linea_id(self, db: AsyncSession, linea_id: int, skip: int = 0, limit: int = 100) -> List[IncidenciaResponse]:
        """Retrieve all Incidencias for a specific Linea."""
        db_incidencias = await self.repository.get_by_linea_id(db, linea_id)
        return [IncidenciaResponse.model_validate(i) for i in db_incidencias]
    
    async def update_incidencia(self, db: AsyncSession, incidencia_id: int, incidencia_in: IncidenciaUpdate) -> Optional[IncidenciaResponse]:
        """Update an Incidencia."""
        db_incidencia = await self.repository.get(db, incidencia_id)
        if db_incidencia:
            db_incidencia = await self.repository.update(db, db_incidencia, incidencia_in)
            return IncidenciaResponse.model_validate(db_incidencia)
        return None
    
    async def delete_incidencia(self, db: AsyncSession, incidencia_id: int) -> bool:
        """Delete an Incidencia."""
        return await self.repository.delete(db, incidencia_id)
