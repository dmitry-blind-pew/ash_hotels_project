from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.auth import UserAddDataSchema, UserHashedSchema
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.get("/me", summary="Узнать кто аутентифицирован сейчас")
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/login", summary="Аутентификация клиента")
async def login_user(user_data: UserAddDataSchema, response: Response, db: DBDep):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегестрирован.")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль.")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register", summary="Регистрация клиента")
async def register_user(user_data: UserAddDataSchema, db: DBDep):
    hashed_password = AuthService().hash_password(user_data.password)
    hashed_user_data = UserHashedSchema(email=user_data.email, hashed_password=hashed_password)
    await db.users.add(hashed_user_data)
    await db.commit()
    return {"status": "User Registered"}


@router.post("/logout", summary="Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "User Logged Out"}