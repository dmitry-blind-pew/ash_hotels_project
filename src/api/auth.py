from fastapi import APIRouter
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.auth import UserAddDataSchema

from passlib.context import CryptContext


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(user_data: UserAddDataSchema):
    hashed_password = pwd_context.hash(user_data.password)
    hashed_user_data = UserAddDataSchema(email=user_data.email, password=hashed_password)
    async with async_session_maker() as session:
        result = await UsersRepository(session).add_user(hashed_user_data)
        await session.commit()
    if result is None:
        return {"status": "Email already exists"}
    return {"status": "User Registered"}