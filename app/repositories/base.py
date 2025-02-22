from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from ..database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: Any) -> Optional[ModelType]:
        """Get a single record by id"""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[ModelType]:
        """Get all records"""
        stmt = select(self.model)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj: CreateSchemaType) -> ModelType:
        """Create a new record"""
        db_obj = self.model(**obj.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, update_data: dict) -> ModelType:
        """Update a record"""
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any) -> bool:
        """Delete a record"""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return True
        return False 