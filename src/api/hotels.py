from fastapi import Query, APIRouter
from models.hotels import HotelsORM
from schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from sqlalchemy import insert, select


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Информация об отелях")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if location is not None:
            query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
        if title is not None:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Hotel deleted"}


@router.post("", summary="Добавление новых отелей")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        add_hotel_statement = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_statement)
        await session.commit()
    return {"status": "Hotel created"}


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