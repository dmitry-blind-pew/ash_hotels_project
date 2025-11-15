from src.models.facilities import FacilitiesORM
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitiesSchema


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = FacilitiesSchema