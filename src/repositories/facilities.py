from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitiesSchema, RoomsFacilitiesSchema


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = FacilitiesSchema


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomsFacilitiesSchema
