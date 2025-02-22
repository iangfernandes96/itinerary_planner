from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class ItineraryQueryBase(BaseModel):
    query: str


class ItineraryQueryCreate(ItineraryQueryBase):
    pass


class ItineraryQueryResponse(ItineraryQueryBase):
    id: UUID
    itinerary_response: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
