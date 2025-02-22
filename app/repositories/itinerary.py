from sqlalchemy.ext.asyncio import AsyncSession
from ..models import ItineraryQuery
from ..schemas import ItineraryQueryCreate
from .base import BaseRepository


class ItineraryRepository(
    BaseRepository[ItineraryQuery, ItineraryQueryCreate]
):
    def __init__(self, db: AsyncSession):
        super().__init__(ItineraryQuery, db)

    async def update_itinerary_response(
        self, db_obj: ItineraryQuery, response: str
    ) -> ItineraryQuery:
        """Update itinerary response"""
        return await self.update(db_obj, {"itinerary_response": response})
