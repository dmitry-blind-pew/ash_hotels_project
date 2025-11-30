from src.mappers.base import DataMapper
from src.models.users import UsersORM
from src.schemas.auth import UserSchema, UserLoginHashedSchema


class UsersMapper(DataMapper):
    db_model = UsersORM
    schema = UserSchema


class UsersMapperHashed(DataMapper):
    db_model = UsersORM
    schema = UserLoginHashedSchema