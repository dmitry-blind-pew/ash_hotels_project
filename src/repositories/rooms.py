from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomSchema

from datetime import date


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = RoomSchema


    async def get_filter_by_date(self, date_from: date, date_to: date, hotel_id):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)
        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))

