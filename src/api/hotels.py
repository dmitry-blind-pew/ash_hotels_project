from fastapi import Query, APIRouter
from src.repositories.hotels import HotelsRepository
from schemas.hotels import Hotel, HotelPatch
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
        

@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Hotel deleted"}


@router.post("", summary="Добавление новых отелей")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": f"Hotel '{hotel}' created"}


@router.put(
    "/{hotel_id}",
    summary="Обновление всех данных отеля",
    description="Необходимо вносить абсолютно все параметры для изменения")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["status"] = hotel_data.status
            return {"status": "Hotel changed"}
    return {"status": "Hotel not found"}


@router.patch("/{hotel_id}", summary="Обновление отдельных параметров отеля")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.status is not None:
                hotel["status"] = hotel_data.status
            return {"status": "Hotel changed"}
    return {"status": "Hotel not found"}