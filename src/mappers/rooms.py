from src.mappers.base import DataMapper
from src.models.rooms import RoomsORM
from src.schemas.rooms import RoomSchema, RoomSchemaWithRelationships


class RoomsMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomSchema


class RoomsMapperWithRelationships(DataMapper):
    db_model = RoomsORM
    schema = RoomSchemaWithRelationships