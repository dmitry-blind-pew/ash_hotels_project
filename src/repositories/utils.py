from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM

from datetime import date
from sqlalchemy.sql import select, func


def rooms_ids_for_booking(date_from: date, date_to: date, hotel_id: int | None = None):
    bookings_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from <= date_to,
            BookingsORM.date_to >= date_from,
        )
        .group_by(BookingsORM.room_id)
        .cte(name="bookings_count")
    )

    free_rooms = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(bookings_count.c.rooms_booked, 0)).label("left_rooms"),
        )
        .select_from(RoomsORM)
        .outerjoin(bookings_count, RoomsORM.id == bookings_count.c.room_id)
        .cte(name="free_rooms")
    )

    rooms_id_for_hotel = select(RoomsORM.id).select_from(RoomsORM)
    if hotel_id is not None:
        rooms_id_for_hotel = rooms_id_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_id_for_hotel.subquery(name="rooms_ids_for_hotel")

    rooms_ids_to_get = (
        select(free_rooms.c.room_id)
        .select_from(free_rooms)
        .filter(free_rooms.c.left_rooms > 0, free_rooms.c.room_id.in_(rooms_ids_for_hotel))
    )

    return rooms_ids_to_get
