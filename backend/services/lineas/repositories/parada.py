"""Repository for Parada model."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.lineas.models.parada import Parada
from .base import BaseRepository


class ParadaRepository(BaseRepository):
    """Repository for Parada CRUD operations."""
    
    def __init__(self):
        super().__init__(Parada)
    
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
    
    async def create(self, db: AsyncSession, obj_in) -> Parada:
        """Create a new Parada, converting GeoJSON geometry to WKT."""
        obj_data = obj_in.model_dump()
        
        # Convert GeoJSON localizacion to WKT format
        if 'localizacion' in obj_data and isinstance(obj_data['localizacion'], dict):
            wkt_geom = self._geojson_to_wkt(obj_data['localizacion'])
            obj_data['localizacion'] = wkt_geom
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, db_obj: Parada, obj_in) -> Parada:
        """Update a Parada, converting GeoJSON geometry to WKT if present."""
        obj_data = obj_in.model_dump(exclude_unset=True)
        
        # Convert GeoJSON localizacion to WKT format if present and valid
        if 'localizacion' in obj_data and obj_data['localizacion'] is not None and isinstance(obj_data['localizacion'], dict) and obj_data['localizacion'].get('type'):
            wkt_geom = self._geojson_to_wkt(obj_data['localizacion'])
            obj_data['localizacion'] = wkt_geom
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_nodo(self, db: AsyncSession, nodo: int) -> Optional[Parada]:
        """Retrieve a Parada by its nodo value."""
        query = select(Parada).where(Parada.nodo == nodo)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def search_by_nombre(self, db: AsyncSession, nombre: str) -> List[Parada]:
        """Search Paradas by name."""
        query = select(Parada).where(Parada.nombre.ilike(f"%{nombre}%"))
        result = await db.execute(query)
        return result.scalars().all()
