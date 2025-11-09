from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomSchemaAddData, RoomPatch, RoomSchemaRequestData, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Информация о номерах отеля")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера по ID")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление номеров отеля")
async def create_room(hotel_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(room_data_and_id)
    await db.commit()
    return {"status": "Room created", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера отеля")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "Room deleted"}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление всех данных номера",
    description="Необходимо вносить абсолютно все параметры для изменения"
)
async def put_room(hotel_id: int, room_id: int, room_data: RoomSchemaRequestData, db: DBDep):
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(id=room_id, update_data=room_data_and_id)
    await db.commit()
    return {"status": "Hotel updated"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Обновление отдельных параметров номера")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    room_data_and_id = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(id=room_id,
                                        hotel_id=hotel_id,
                                        update_data=room_data_and_id,
                                        exclude_unset=True)
    await db.commit()
    return {"status": "Room updated"}