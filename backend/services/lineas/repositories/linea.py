"""Repository for Linea model."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from services.lineas.models.linea import Linea
from .base import BaseRepository


class LineaRepository(BaseRepository):
    """Repository for Linea CRUD operations."""
    
    def __init__(self):
        super().__init__(Linea)
    
    @staticmethod
    def _geojson_to_wkt(geojson_geom: dict) -> str:
        """Convert GeoJSON geometry to WKT format.
        
        Supports:
        - Point: {'type': 'Point', 'coordinates': [lon, lat]}
        - LineString: {'type': 'LineString', 'coordinates': [[lon, lat], ...]}
        
        Args:
            geojson_geom: GeoJSON geometry dictionary
            
        Returns:
            WKT string
        """
        geom_type = geojson_geom.get('type')
        coords = geojson_geom.get('coordinates', [])
        
        if geom_type == 'LineString':
            # LineString: coordinates is a list of [lon, lat]
            coord_str = ', '.join([f"{lon} {lat}" for lon, lat in coords])
            return f"LINESTRING({coord_str})"
        elif geom_type == 'Point':
            # Point: coordinates is [lon, lat]
            return f"POINT({coords[0]} {coords[1]})"
        else:
            raise ValueError(f"Unsupported geometry type: {geom_type}")
    
    async def create(self, db: AsyncSession, obj_in) -> Linea:
        """Create a new Linea, converting GeoJSON geometry to WKT."""
        obj_data = obj_in.model_dump()
        
        # Convert GeoJSON recorrido to WKT format
        if 'recorrido' in obj_data and isinstance(obj_data['recorrido'], dict):
            wkt_geom = self._geojson_to_wkt(obj_data['recorrido'])
            obj_data['recorrido'] = wkt_geom
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, db_obj: Linea, obj_in) -> Linea:
        """Update a Linea, converting GeoJSON geometry to WKT if present."""
        obj_data = obj_in.model_dump(exclude_unset=True)
        
        # Convert GeoJSON recorrido to WKT format if present and valid
        if 'recorrido' in obj_data and obj_data['recorrido'] is not None and isinstance(obj_data['recorrido'], dict) and obj_data['recorrido'].get('type'):
            wkt_geom = self._geojson_to_wkt(obj_data['recorrido'])
            obj_data['recorrido'] = wkt_geom
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_numero(self, db: AsyncSession, linea: int) -> Optional[Linea]:
        """Retrieve a Linea by its line number."""
        query = select(Linea).where(Linea.linea == linea)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def search_by_nombre(self, db: AsyncSession, nombre: str) -> List[Linea]:
        """Search Lineas by name."""
        query = select(Linea).where(Linea.nombreLinea.ilike(f"%{nombre}%"))
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_labelLinea(self, db: AsyncSession, labelLinea: str) -> Optional[Linea]:
        """Retrieve a Linea by its labelLinea identifier."""
        query = select(Linea).where(Linea.labelLinea == labelLinea)
        result = await db.execute(query)
        return result.scalar_one_or_none()
