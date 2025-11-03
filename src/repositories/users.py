from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.auth import UserAddDataSchema
from pydantic import BaseModel


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = UserAddDataSchema

    async def add_user(self, data: BaseModel):
        is_user = await self.get_one_or_none(email=data.email)
        if is_user is None:
            return await self.add(data=data)
        return None
