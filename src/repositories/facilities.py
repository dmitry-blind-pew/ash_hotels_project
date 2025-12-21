from sqlalchemy.exc import NoResultFound

from src.exeptions import ObjectNotFoundException
from src.mappers.facilities import FacilitiesMapper, RoomsFacilitiesMapper
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import RoomsFacilitiesAddSchema


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilitiesMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomsFacilitiesMapper

    async def update_facilities(self, room_id: int, new_facilities_ids: list[int]):
        try:
            facilities_now = await self.get_all(rooms=room_id)
        except NoResultFound:
            raise ObjectNotFoundException
        list_facilities_now = [f.facilities for f in facilities_now]
        facilities_to_add = list(set(new_facilities_ids) - set(list_facilities_now))
        facilities_to_delete = list(set(list_facilities_now) - set(new_facilities_ids))

        rooms_facilities_add_data = [
            RoomsFacilitiesAddSchema(rooms=room_id, facilities=facility_id) for facility_id in facilities_to_add
        ]
        await self.add_bulk(rooms_facilities_add_data)

        for delete_facility in facilities_to_delete:
            await self.delete(rooms=room_id, facilities=delete_facility)
