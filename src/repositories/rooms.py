from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = RoomSchema
