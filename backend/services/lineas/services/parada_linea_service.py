"""Service layer for ParadaLinea CRUD operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from services.lineas.schemas import (
    ParadaLineaCreate,
    ParadaLineaUpdate,
    ParadaLineaResponse,
)
from services.lineas.repositories import ParadaLineaRepository


class ParadaLineaService:
    """Service for ParadaLinea operations."""
    
    def __init__(self):
        self.repository = ParadaLineaRepository()
    
    async def create_parada_linea(self, db: AsyncSession, parada_linea_in: ParadaLineaCreate) -> ParadaLineaResponse:
        """Create a new ParadaLinea relationship."""
        db_parada_linea = await self.repository.create(db, parada_linea_in)
        return ParadaLineaResponse.model_validate(db_parada_linea)
    
    async def get_parada_linea(self, db: AsyncSession, parada_linea_id: int) -> Optional[ParadaLineaResponse]:
        """Retrieve a ParadaLinea by ID."""
        db_parada_linea = await self.repository.get(db, parada_linea_id)
        if db_parada_linea:
            return ParadaLineaResponse.model_validate(db_parada_linea)
        return None
    
    async def get_all_parada_lineas(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ParadaLineaResponse]:
        """Retrieve all ParadaLinea relationships."""
        db_parada_lineas = await self.repository.get_all(db, skip, limit)
        return [ParadaLineaResponse.model_validate(pl) for pl in db_parada_lineas]
    
    async def update_parada_linea(
        self, db: AsyncSession, parada_linea_id: int, parada_linea_in: ParadaLineaUpdate
    ) -> Optional[ParadaLineaResponse]:
        """Update a ParadaLinea relationship."""
        db_parada_linea = await self.repository.get(db, parada_linea_id)
        if db_parada_linea:
            db_parada_linea = await self.repository.update(db, db_parada_linea, parada_linea_in)
            return ParadaLineaResponse.model_validate(db_parada_linea)
        return None
    
    async def delete_parada_linea(self, db: AsyncSession, parada_linea_id: int) -> bool:
        """Delete a ParadaLinea relationship."""
        return await self.repository.delete(db, parada_linea_id)
    
    async def get_parada_lineas_by_parada(self, db: AsyncSession, parada_id: int) -> List[ParadaLineaResponse]:
        """Get all Lineas for a specific Parada."""
        db_parada_lineas = await self.repository.get_by_parada(db, parada_id)
        return [ParadaLineaResponse.model_validate(pl) for pl in db_parada_lineas]
    
    async def get_parada_lineas_by_linea(self, db: AsyncSession, linea_id: int) -> List[ParadaLineaResponse]:
        """Get all Paradas for a specific Linea."""
        db_parada_lineas = await self.repository.get_by_linea(db, linea_id)
        return [ParadaLineaResponse.model_validate(pl) for pl in db_parada_lineas]
    
    async def get_parada_linea_relationship(
        self, db: AsyncSession, parada_id: int, linea_id: int
    ) -> Optional[ParadaLineaResponse]:
        """Get a specific ParadaLinea relationship."""
        db_parada_linea = await self.repository.get_by_parada_and_linea(db, parada_id, linea_id)
        if db_parada_linea:
            return ParadaLineaResponse.model_validate(db_parada_linea)
        return None
