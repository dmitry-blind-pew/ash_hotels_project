from fastapi import Query, APIRouter
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelSchemaAddData, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Информация об отелях")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(title=title, 
                                                       location=location, 
                                                       limit=per_page, 
                                                       offset=per_page * (pagination.page - 1))


@router.get("{hotel_id}", summary="Поиск отеля по ID")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"Hotel deleted"}


@router.post("", summary="Добавление новых отелей")
async def create_hotel(hotel_data: HotelSchemaAddData):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "Hotel created", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновление всех данных отеля",
    description="Необходимо вносить абсолютно все параметры для изменения")
async def put_hotel(hotel_id: int, hotel_data: HotelSchemaAddData):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(id=hotel_id, update_data=hotel_data)
        await session.commit()
    return {"status": "Hotel updated"}


@router.patch("/{hotel_id}", summary="Обновление отдельных параметров отеля")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(id=hotel_id, update_data=hotel_data, exclude_unset=True)
        await session.commit()
    return {"status": "Hotel updated"}
