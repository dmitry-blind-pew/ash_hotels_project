from fastapi import Query, APIRouter, HTTPException
from datetime import date
from fastapi_cache.decorator import cache

from src.exeptions import ObjectNotFoundException
from src.schemas.hotels import HotelSchemaAddData, HotelPatch
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelsService


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Информация об отелях")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(example="2025-11-11"),
    date_to: date = Query(example="2025-11-12"),
):
    return await HotelsService(db).get_hotels(pagination, title, location, date_from, date_to)


@router.get("{hotel_id}", summary="Поиск отеля по ID")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelsService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Отеля не существует")


@router.post("", summary="Добавление отелей")
async def create_hotel(hotel_data: HotelSchemaAddData, db: DBDep):
    hotel = await HotelsService(db).create_hotel(hotel_data)
    return {"status": "Hotel created", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновление всех данных отеля",
    description="Необходимо вносить абсолютно все параметры для изменения",
)
async def put_hotel(hotel_id: int, hotel_data: HotelSchemaAddData, db: DBDep):
    await HotelsService(db).put_hotel(hotel_id, hotel_data)
    return {"status": "Hotel updated"}


@router.patch("/{hotel_id}", summary="Обновление отдельных параметров отеля")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelsService(db).patch_hotel(hotel_id, hotel_data)
    return {"status": "Hotel updated"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelsService(db).delete_hotel(hotel_id)
    return {"Hotel deleted"}
