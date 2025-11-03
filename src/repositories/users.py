from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.auth import UserAddDataSchema


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = UserAddDataSchema


