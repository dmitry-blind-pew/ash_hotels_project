from fastapi import APIRouter, Query
from datetime import date
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exeptions import RoomNotFoundException, RoomNotFoundHTTPException, HotelNotFoundException, HotelNotFoundHTTPException
from src.schemas.rooms import (
    RoomSchemaRequestData,
    RoomSchemaPatchRequest,
)
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Информация о номерах отеля")
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-11-11"),
    date_to: date = Query(example="2025-11-12"),
):
    return await RoomService(db).get_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера по ID")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(room_id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Добавление номеров отеля")
async def create_room(hotel_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "Room created", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление всех данных номера",
    description="Необходимо вносить абсолютно все параметры для изменения",
)
async def put_room(hotel_id: int, room_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    try:
        await RoomService(db).put_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "Room updated"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Обновление отдельных параметров номера")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomSchemaPatchRequest, db: DBDep):
    try:
        await RoomService(db).patch_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "Room updated"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера отеля")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "Room deleted"}
