from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exeptions import (
    UserAlreadyExistsHTTPException,
    UserAlreadyExistsException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
)
from src.schemas.auth import UserAddDataSchema
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.get("/me", summary="Узнать кто аутентифицирован сейчас")
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await AuthService(db).get_me(user_id=user_id)
    return user


@router.post("/login", summary="Аутентификация клиента")
async def login_user(user_data: UserAddDataSchema, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(user_data)
    except EmailNotRegisteredException as exc:
        raise EmailNotRegisteredHTTPException from exc
    except IncorrectPasswordException as exc:
        raise IncorrectPasswordHTTPException from exc
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register", summary="Регистрация клиента")
async def register_user(user_data: UserAddDataSchema, db: DBDep):
    try:
        await AuthService(db).register_user(user_data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "User Registered"}


@router.post("/logout", summary="Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "User Logged Out"}
