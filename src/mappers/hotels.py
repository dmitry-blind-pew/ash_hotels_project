from src.mappers.base import DataMapper
from src.models.hotels import HotelsORM
from src.schemas.hotels import HotelSchema


class HotelsMapper(DataMapper):
    db_model = HotelsORM
    schema = HotelSchema