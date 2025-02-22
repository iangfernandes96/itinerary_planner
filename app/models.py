from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid6

from .database import Base


class ItineraryQuery(Base):
    __tablename__ = "itinerary_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7)
    query = Column(String, nullable=False)
    itinerary_response = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())
