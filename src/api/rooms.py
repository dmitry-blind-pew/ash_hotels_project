from fastapi import APIRouter
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomSchemaAddData, RoomPatch, RoomSchemaRequestData, RoomPatchRequest
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Информация о номерах отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Поиск номера по ID")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление номеров отеля")
async def create_room(hotel_id: int, room_data: RoomSchemaRequestData):
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data_and_id)
        await session.commit()
    return {"status": "Room created", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера отеля")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "Room deleted"}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновление всех данных номера",
    description="Необходимо вносить абсолютно все параметры для изменения"
)
async def put_room(hotel_id: int, room_id: int, room_data: RoomSchemaRequestData):
    room_data_and_id = RoomSchemaAddData(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, update_data=room_data_and_id)
        await session.commit()
    return {"status": "Hotel updated"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Обновление отдельных параметров номера")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    room_data_and_id = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id,
                                            hotel_id=hotel_id,
                                            update_data=room_data_and_id,
                                            exclude_unset=True)
        await session.commit()
    return {"status": "Room updated"}