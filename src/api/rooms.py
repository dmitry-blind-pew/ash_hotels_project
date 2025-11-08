from fastapi import APIRouter
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomSchemaAddData, RoomPatch
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Информация о номерах отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id)


@router.get("/rooms/{room_id}", summary="Поиск номера по ID")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/rooms", summary="Добавление номеров отеля")
async def create_room(room_data: RoomSchemaAddData):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "Room created", "data": room}


@router.delete("/rooms/{room_id}", summary="Удаление номера отеля")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "Room deleted"}


@router.put(
    "/rooms/{room_id}",
    summary="Обновление всех данных номера",
    description="Необходимо вносить абсолютно все параметры для изменения"
)
async def put_room(room_id: int, room_data: RoomSchemaAddData):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, update_data=room_data)
        await session.commit()
    return {"status": "Hotel updated"}


@router.patch("/rooms/{room_id}", summary="Обновление отдельных параметров номера")
async def patch_room(room_id: int, room_data: RoomPatch):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, update_data=room_data, exclude_unset=True)
        await session.commit()
    return {"status": "Room updated"}