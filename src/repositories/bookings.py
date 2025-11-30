from sqlalchemy import select
from datetime import date

from src.mappers.bookings import BookingsMapper
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingsMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        bookings = result.scalars().all()
        return [self.mapper.map_to_domain_entity(booking) for booking in bookings]
