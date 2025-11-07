from typing import Annotated
from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Страница")]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="Количество элементов на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_access_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(status_code=401, detail="Нет токена доступа")
    return access_token

def get_current_user_id(access_token: str = Depends(get_access_token)) -> int:
    user_token_data = AuthService().decode_access_token(access_token)
    return user_token_data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]