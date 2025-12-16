from fastapi import APIRouter, Query, HTTPException
from datetime import date
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exeptions import ObjectNotFoundException, UserExistsException
from src.schemas.facilities import RoomsFacilitiesAddSchema
from src.schemas.rooms import (
    RoomSchemaAddData,
    RoomSchemaPatch,
    RoomSchemaRequestData,
    RoomSchemaPatchRequest,
)


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Информация о номерах отеля")
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-11-11"),
    date_to: date = Query(example="2025-11-12"),
):
    if date_from > date_to:
        raise HTTPException(status_code=409, detail="Дата выезда позже даты заезда")
    return await db.rooms.get_rooms_filter_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера по ID")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номера не существует")


@router.post("/{hotel_id}/rooms", summary="Добавление номеров отеля")
async def create_room(hotel_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(room_data_and_id)
    except UserExistsException:
        raise HTTPException(status_code=404, detail="Такого отеля не существует")

    rooms_facilities_data = [
        RoomsFacilitiesAddSchema(rooms=room.id, facilities=facility_id)
        for facility_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "Room created", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление всех данных номера",
    description="Необходимо вносить абсолютно все параметры для изменения",
)
async def put_room(hotel_id: int, room_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    room_data_without_facilities = room_data.model_dump(exclude={"facilities_ids"})
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data_without_facilities)
    try:
        await db.rooms.edit(id=room_id, update_data=room_data_and_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Такого номера не существует")

    await db.rooms_facilities.update_facilities(
        room_id=room_id, new_facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "Room updated"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Обновление отдельных параметров номера")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomSchemaPatchRequest, db: DBDep):
    try:
        await db.rooms_facilities.update_facilities(room_id=room_id, new_facilities_ids=room_data.facilities_ids)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Такого номера не существует")

    room_data_dict = room_data.model_dump(exclude_unset=True, exclude={"facilities_ids"})
    room_data_and_id = RoomSchemaPatch(hotel_id=hotel_id, **room_data_dict)
    try:
        await db.rooms.edit(id=room_id, hotel_id=hotel_id, update_data=room_data_and_id, exclude_unset=True)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Такого номера не существует")
    await db.commit()
    return {"status": "Room updated"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера отеля")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Такого номера не существует")
    await db.commit()
    return {"status": "Room deleted"}
