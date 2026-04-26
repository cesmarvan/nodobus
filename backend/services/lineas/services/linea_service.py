"""Service layer for Linea CRUD operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from services.lineas.schemas import (
    LineaCreate,
    LineaUpdate,
    LineaResponse,
)
from services.lineas.repositories import LineaRepository


class LineaService:
    """Service for Linea operations."""
    
    def __init__(self):
        self.repository = LineaRepository()
    
    async def create_linea(self, db: AsyncSession, linea_in: LineaCreate) -> LineaResponse:
        """Create a new Linea."""
        db_linea = await self.repository.create(db, linea_in)
        return LineaResponse.model_validate(db_linea)
    
    async def get_linea(self, db: AsyncSession, linea_id: int) -> Optional[LineaResponse]:
        """Retrieve a Linea by ID."""
        db_linea = await self.repository.get(db, linea_id)
        if db_linea:
            return LineaResponse.model_validate(db_linea)
        return None
    
    async def get_all_lineas(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[LineaResponse]:
        """Retrieve all Lineas."""
        db_lineas = await self.repository.get_all(db, skip, limit)
        return [LineaResponse.model_validate(l) for l in db_lineas]
    
    async def update_linea(self, db: AsyncSession, linea_id: int, linea_in: LineaUpdate) -> Optional[LineaResponse]:
        """Update a Linea."""
        db_linea = await self.repository.get(db, linea_id)
        if db_linea:
            db_linea = await self.repository.update(db, db_linea, linea_in)
            return LineaResponse.model_validate(db_linea)
        return None
    
    async def delete_linea(self, db: AsyncSession, linea_id: int) -> bool:
        """Delete a Linea."""
        return await self.repository.delete(db, linea_id)
    
    async def get_linea_by_numero(self, db: AsyncSession, linea: int) -> Optional[LineaResponse]:
        """Get a Linea by its line number."""
        db_linea = await self.repository.get_by_numero(db, linea)
        if db_linea:
            return LineaResponse.model_validate(db_linea)
        return None
    
    async def search_lineas_by_nombre(self, db: AsyncSession, nombre: str) -> List[LineaResponse]:
        """Search Lineas by name."""
        db_lineas = await self.repository.search_by_nombre(db, nombre)
        return [LineaResponse.model_validate(l) for l in db_lineas]
    
    async def get_linea_by_labelLinea(self, db: AsyncSession, labelLinea: str) -> Optional[LineaResponse]:
        """Get a Linea by its label identifier."""
        db_linea = await self.repository.get_by_labelLinea(db, labelLinea)
        if db_linea:
            return LineaResponse.model_validate(db_linea)
        return None
