from fastapi import APIRouter, Query
from datetime import date

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacilitiesAddSchema
from src.schemas.rooms import RoomSchemaAddData, RoomSchemaPatch, RoomSchemaRequestData, RoomSchemaPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Информация о номерах отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-11-11"),
        date_to: date = Query(example="2025-11-12")):
    return await db.rooms.get_rooms_filter_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера по ID")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление номеров отеля")
async def create_room(hotel_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(room_data_and_id)

    rooms_facilities_data = [RoomsFacilitiesAddSchema(rooms=room.id, facilities=facility_id) for facility_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "Room created", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление всех данных номера",
    description="Необходимо вносить абсолютно все параметры для изменения"
)
async def put_room(hotel_id: int, room_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    facilities_now = await db.rooms_facilities.get_all(rooms=room_id)
    list_facilities_now = [f.facilities for f in facilities_now]
    facilities_to_add = list(set(room_data.facilities_ids) - set(list_facilities_now))
    facilities_to_delete = list(set(list_facilities_now) - set(room_data.facilities_ids))

    room_data_without_facilities = room_data.model_dump(exclude={'facilities_ids'})
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data_without_facilities)
    await db.rooms.edit(id=room_id, update_data=room_data_and_id)

    rooms_facilities_add_data = [RoomsFacilitiesAddSchema(rooms=room_id, facilities=facility_id) for facility_id in
                             facilities_to_add]
    await db.rooms_facilities.add_bulk(rooms_facilities_add_data)

    for delete_facility in facilities_to_delete:
        await db.rooms_facilities.delete(rooms=room_id, facilities=delete_facility)

    await db.commit()
    return {"status": "Room updated"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Обновление отдельных параметров номера")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomSchemaPatchRequest, db: DBDep):
    if room_data.facilities_ids:
        facilities_now = await db.rooms_facilities.get_all(rooms=room_id)
        list_facilities_now = [f.facilities for f in facilities_now]
        facilities_to_add = list(set(room_data.facilities_ids) - set(list_facilities_now))
        facilities_to_delete = list(set(list_facilities_now) - set(room_data.facilities_ids))

        rooms_facilities_add_data = [RoomsFacilitiesAddSchema(rooms=room_id, facilities=facility_id) for facility_id in
                                     facilities_to_add]
        await db.rooms_facilities.add_bulk(rooms_facilities_add_data)

        for delete_facility in facilities_to_delete:
            await db.rooms_facilities.delete(rooms=room_id, facilities=delete_facility)

    room_data_dict = room_data.model_dump(exclude_unset=True, exclude={'facilities_ids'})
    room_data_and_id = RoomSchemaPatch(hotel_id=hotel_id, **room_data_dict)
    await db.rooms.edit(
        id=room_id,
        hotel_id=hotel_id,
        update_data=room_data_and_id,
        exclude_unset=True
    )
    await db.commit()
    return {"status": "Room updated"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера отеля")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "Room deleted"}

