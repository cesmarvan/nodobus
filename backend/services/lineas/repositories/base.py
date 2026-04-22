"""Base repository with common CRUD operations."""

from typing import Generic, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")


class BaseRepository(Generic[ModelType, CreateSchemaType]):
    """Base repository for common CRUD operations."""
    
    def __init__(self, model):
        self.model = model
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object in the database."""
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """Retrieve an object by ID."""
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Retrieve all objects with pagination."""
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Update an existing object."""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Delete an object by ID."""
        db_obj = await self.get(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.flush()
            return True
        return False
