"""Service layer for Parada CRUD operations."""

from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from services.lineas.schemas import (
    ParadaCreate,
    ParadaUpdate,
    ParadaResponse,
)
from services.lineas.repositories import ParadaRepository


class ParadaService:
    """Service for Parada operations."""
    
    def __init__(self):
        self.repository = ParadaRepository()
    
    async def create_parada(self, db: AsyncSession, parada_in: ParadaCreate) -> ParadaResponse:
        """Create a new Parada."""
        db_parada = await self.repository.create(db, parada_in)
        return ParadaResponse.model_validate(db_parada)
    
    async def get_parada(self, db: AsyncSession, parada_id: int) -> Optional[ParadaResponse]:
        """Retrieve a Parada by ID."""
        db_parada = await self.repository.get(db, parada_id)
        if db_parada:
            return ParadaResponse.model_validate(db_parada)
        return None
    
    async def get_all_paradas(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ParadaResponse]:
        """Retrieve all Paradas."""
        db_paradas = await self.repository.get_all(db, skip, limit)
        return [ParadaResponse.model_validate(p) for p in db_paradas]
    
    async def update_parada(self, db: AsyncSession, parada_id: int, parada_in: ParadaUpdate) -> Optional[ParadaResponse]:
        """Update a Parada."""
        db_parada = await self.repository.get(db, parada_id)
        if db_parada:
            db_parada = await self.repository.update(db, db_parada, parada_in)
            return ParadaResponse.model_validate(db_parada)
        return None
    
    async def delete_parada(self, db: AsyncSession, parada_id: int) -> bool:
        """Delete a Parada."""
        return await self.repository.delete(db, parada_id)
    
    async def get_parada_by_nodo(self, db: AsyncSession, nodo: int) -> Optional[ParadaResponse]:
        """Get a Parada by nodo value."""
        db_parada = await self.repository.get_by_nodo(db, nodo)
        if db_parada:
            return ParadaResponse.model_validate(db_parada)
        return None
    
    async def search_paradas_by_nombre(self, db: AsyncSession, nombre: str) -> List[ParadaResponse]:
        """Search Paradas by name."""
        db_paradas = await self.repository.search_by_nombre(db, nombre)
        return [ParadaResponse.model_validate(p) for p in db_paradas]
