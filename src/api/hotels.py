from fastapi import Query, APIRouter
from src.schemas.hotel import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
import math


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 0, "title": "Vilnus", "status": "open"},
    {"id": 1, "title": "Barselona", "status": "close"},
    {"id": 2, "title": "Munich", "status": "open"},
    {"id": 3, "title": "Valensia", "status": "open"},
    {"id": 4, "title": "Minsk", "status": "close"},
    {"id": 5, "title": "Milan", "status": "open"},
    {"id": 6, "title": "Roma", "status": "open"},
    {"id": 7, "title": "Berlin", "status": "close"},
    {"id": 8, "title": "Warshava", "status": "open"},
]


@router.get("", summary="Информация об отелях")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="ID"), 
    title: str | None = Query(None, description="Название отеля")
):
    if id is not None and title is not None:
        result = [hotel for hotel in hotels if hotel["id"] == id and hotel["title"] == title]
    if id is not None:
        result = [hotel for hotel in hotels if hotel["id"] == id]
    if title is not None:
        result = [hotel for hotel in hotels if hotel["title"] == title]
    else:
        result = hotels
    
    if len(result) > pagination.per_page and pagination.page <= math.ceil(len(result) / pagination.per_page):
        if pagination.page * pagination.per_page > len(result):
            return result[(pagination.page - 1) * pagination.per_page :]
        return result[(pagination.page - 1) * pagination.per_page : pagination.page * pagination.per_page]
    return []


@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Hotel deleted"}


@router.post("", summary="Добавление новых отелей")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": hotel_data.title, "status": hotel_data.status})
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