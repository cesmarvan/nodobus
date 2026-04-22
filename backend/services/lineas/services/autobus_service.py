"""Service layer for Autobus CRUD operations."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from services.lineas.schemas import (
    AutobusCreate,
    AutobusUpdate,
    AutobusResponse,
)
from services.lineas.repositories import AutobusRepository


class AutobusService:
    """Service for Autobus operations."""
    
    def __init__(self):
        self.repository = AutobusRepository()
    
    async def create_autobus(self, db: AsyncSession, autobus_in: AutobusCreate) -> AutobusResponse:
        """Create a new Autobus."""
        db_autobus = await self.repository.create(db, autobus_in)
        return AutobusResponse.model_validate(db_autobus)
    
    async def get_autobus(self, db: AsyncSession, autobus_id: int) -> Optional[AutobusResponse]:
        """Retrieve an Autobus by ID."""
        db_autobus = await self.repository.get(db, autobus_id)
        if db_autobus:
            return AutobusResponse.model_validate(db_autobus)
        return None
    
    async def get_all_autobuses(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[AutobusResponse]:
        """Retrieve all Autobuses."""
        db_autobuses = await self.repository.get_all(db, skip, limit)
        return [AutobusResponse.model_validate(a) for a in db_autobuses]
    
    async def update_autobus(self, db: AsyncSession, autobus_id: int, autobus_in: AutobusUpdate) -> Optional[AutobusResponse]:
        """Update an Autobus."""
        db_autobus = await self.repository.get(db, autobus_id)
        if db_autobus:
            db_autobus = await self.repository.update(db, db_autobus, autobus_in)
            return AutobusResponse.model_validate(db_autobus)
        return None
    
    async def delete_autobus(self, db: AsyncSession, autobus_id: int) -> bool:
        """Delete an Autobus."""
        return await self.repository.delete(db, autobus_id)
    
    async def get_autobus_by_vehiculo(self, db: AsyncSession, vehiculo: int) -> Optional[AutobusResponse]:
        """Get an Autobus by its vehicle identifier."""
        db_autobus = await self.repository.get_by_vehiculo(db, vehiculo)
        if db_autobus:
            return AutobusResponse.model_validate(db_autobus)
        return None
    
    async def get_autobuses_by_linea(self, db: AsyncSession, linea_id: int) -> List[AutobusResponse]:
        """Get all Autobuses for a specific Linea."""
        db_autobuses = await self.repository.get_by_linea(db, linea_id)
        return [AutobusResponse.model_validate(a) for a in db_autobuses]
    
    async def get_autobuses_by_sentido(self, db: AsyncSession, sentido: int) -> List[AutobusResponse]:
        """Get all Autobuses with a specific direction."""
        db_autobuses = await self.repository.get_by_sentido(db, sentido)
        return [AutobusResponse.model_validate(a) for a in db_autobuses]
