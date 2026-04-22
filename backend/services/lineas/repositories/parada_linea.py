"""Repository for ParadaLinea model."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.lineas.models.paradaLinea import ParadaLinea
from .base import BaseRepository


class ParadaLineaRepository(BaseRepository):
    """Repository for ParadaLinea CRUD operations."""
    
    def __init__(self):
        super().__init__(ParadaLinea)
    
    async def get_by_parada(self, db: AsyncSession, parada_id: int) -> List[ParadaLinea]:
        """Get all ParadaLinea records for a specific Parada."""
        query = select(ParadaLinea).where(ParadaLinea.parada_id == parada_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_linea(self, db: AsyncSession, linea_id: int) -> List[ParadaLinea]:
        """Get all ParadaLinea records for a specific Linea."""
        query = select(ParadaLinea).where(ParadaLinea.linea_id == linea_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_parada_and_linea(
        self, db: AsyncSession, parada_id: int, linea_id: int
    ) -> Optional[ParadaLinea]:
        """Get a specific ParadaLinea relationship."""
        query = select(ParadaLinea).where(
            (ParadaLinea.parada_id == parada_id) & (ParadaLinea.linea_id == linea_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
