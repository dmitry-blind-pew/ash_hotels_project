from src.mappers.base import DataMapper
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import FacilitiesSchema, RoomsFacilitiesSchema, RoomsFacilitiesAddSchema


class FacilitiesMapper(DataMapper):
    db_model = FacilitiesORM
    schema = FacilitiesSchema


class RoomsFacilitiesMapper(DataMapper):
    db_model = RoomsFacilitiesORM
    schema = RoomsFacilitiesSchema

