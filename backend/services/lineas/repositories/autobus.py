"""Repository for Autobus model."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.lineas.models.autobus import Autobus
from .base import BaseRepository


class AutobusRepository(BaseRepository):
    """Repository for Autobus CRUD operations."""
    
    def __init__(self):
        super().__init__(Autobus)
    
    @staticmethod
    def _geojson_to_wkt(geojson_point: dict) -> str:
        """Convert GeoJSON Point to WKT format.
        
        Args:
            geojson_point: Dictionary with 'type' and 'coordinates' [longitude, latitude]
            
        Returns:
            WKT string in format "POINT(longitude latitude)"
        """
        coords = geojson_point['coordinates']  # [longitude, latitude]
        return f"POINT({coords[0]} {coords[1]})"
    
    async def create(self, db: AsyncSession, obj_in) -> Autobus:
        """Create a new Autobus, converting GeoJSON geometry to WKT."""
        obj_data = obj_in.model_dump()
        
        # Convert GeoJSON posicion to WKT format
        if 'posicion' in obj_data and isinstance(obj_data['posicion'], dict):
            wkt_geom = self._geojson_to_wkt(obj_data['posicion'])
            obj_data['posicion'] = wkt_geom
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, db_obj: Autobus, obj_in) -> Autobus:
        """Update an Autobus, converting GeoJSON geometry to WKT if present."""
        obj_data = obj_in.model_dump(exclude_unset=True)
        
        # Convert GeoJSON posicion to WKT format if present and valid
        if 'posicion' in obj_data and obj_data['posicion'] is not None and isinstance(obj_data['posicion'], dict) and obj_data['posicion'].get('type'):
            wkt_geom = self._geojson_to_wkt(obj_data['posicion'])
            obj_data['posicion'] = wkt_geom
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_vehiculo(self, db: AsyncSession, vehiculo: int) -> Optional[Autobus]:
        """Retrieve an Autobus by its vehicle identifier."""
        query = select(Autobus).where(Autobus.vehiculo == vehiculo)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_linea(self, db: AsyncSession, linea_id: int) -> List[Autobus]:
        """Get all Autobuses for a specific Linea."""
        query = select(Autobus).where(Autobus.linea_id == linea_id)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_sentido(self, db: AsyncSession, sentido: int) -> List[Autobus]:
        """Get all Autobuses with a specific direction."""
        query = select(Autobus).where(Autobus.sentido == sentido)
        result = await db.execute(query)
        return result.scalars().all()
