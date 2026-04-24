"""Repository for Incidencia model."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.incidencias.models.incidencia import Incidencia
from .base import BaseRepository


class IncidenciaRepository(BaseRepository):
    """Repository for incidencia CRUD operations."""
    
    def __init__(self):
        super().__init__(Incidencia)
    
    
    async def create(self, db: AsyncSession, obj_in) -> Incidencia:
        """Create a new Incidencia."""
        obj_data = obj_in.model_dump()
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, db_obj: Incidencia, obj_in) -> Incidencia:
        """Update a Incidencia."""
        obj_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_parada_id(self, db: AsyncSession, parada_id: int) -> List[Incidencia]:
        """Retrieve Incidencias by parada_id."""
        query = select(Incidencia).where(Incidencia.parada_id == parada_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_linea_id(self, db: AsyncSession, linea_id: int) -> List[Incidencia]:
        """Retrieve Incidencias by linea_id."""
        query = select(Incidencia).where(Incidencia.linea_id == linea_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def delete(self, db: AsyncSession, id: int) -> None:
        """Delete a Incidencia by its ID."""
        await super().delete(db, id)
