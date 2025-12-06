from datetime import date

from src.schemas.bookings import BookingSchemaAddRequest


async def test_booking_crud(db_manager):
    user_id = (await db_manager.users.get_all())[0].id
    room_id = (await db_manager.rooms.get_all())[0].id
    booking_data = BookingSchemaAddRequest(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=12, day=5),
        date_to=date(year=2025, month=12, day=6),
        price=100
    )
    create_result = await db_manager.bookings.add(booking_data)
    print(f"РЕЗУЛЬТАТ С {create_result}")

    read_result = await db_manager.bookings.get_one_or_none(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=12, day=5),
        date_to=date(year=2025, month=12, day=6)
    )
    print(f"РЕЗУЛЬТАТ R {read_result}")

    update_date = BookingSchemaAddRequest(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=12, day=5),
        date_to=date(year=2025, month=12, day=7),
        price=100
    )
    booking_id = read_result.id
    await db_manager.bookings.edit(update_data=update_date, exclude_unset=True, id=booking_id)
    update_result =await db_manager.bookings.get_one_or_none(id=booking_id)
    print(f"РЕЗУЛЬТАТ U {update_result}")

    await db_manager.bookings.delete(id=booking_id)
    delete_result = await db_manager.bookings.get_one_or_none(id=booking_id)
    print(f"РЕЗУЛЬТАТ D {delete_result}")
    await db_manager.commit()