from sqlalchemy import Column, String, DateTime, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
import uuid6

from .database import Base


class ItineraryQuery(Base):
    __tablename__ = "itinerary_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7)
    query = Column(String, nullable=False)
    itinerary_response = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs) -> "ItineraryQuery":
        """Create a new itinerary query"""
        query = cls(**kwargs)
        db.add(query)
        await db.commit()
        await db.refresh(query)
        return query

    @classmethod
    async def get(cls, db: AsyncSession, id: str) -> "ItineraryQuery | None":
        """Get an itinerary query by ID"""
        return await db.get(cls, id)

    @classmethod
    async def get_all(cls, db: AsyncSession) -> list["ItineraryQuery"]:
        """Get all itinerary queries"""
        result = await db.execute(select(cls))
        return list(result.scalars().all())

    async def update_response(
        self, db: AsyncSession, response: str
    ) -> "ItineraryQuery":
        """Update the itinerary response"""
        self.itinerary_response = response
        await db.commit()
        await db.refresh(self)
        return self
