from sqlalchemy import select
from datetime import date

from src.exeptions import AllRoomsAreBookedException
from src.mappers.bookings import BookingsMapper
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingsMapper

    async def get_bookings_with_today_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        bookings = result.scalars().all()
        return [self.mapper.map_to_domain_entity(booking) for booking in bookings]

    async def add_booking(self, data, hotel_id):
        free_rooms_ids = rooms_ids_for_booking(date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id)
        free_rooms_result = await self.session.execute(free_rooms_ids)
        free_rooms = free_rooms_result.scalars().all()

        if data.room_id not in free_rooms:
            raise AllRoomsAreBookedException
        return await self.add(data)
