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
    assert create_result
    assert create_result.room_id == room_id
    assert create_result.user_id == user_id
    assert create_result.date_from == date(year=2025, month=12, day=5)
    assert create_result.date_to == date(year=2025, month=12, day=6)
    assert create_result.price == 100
    print(f"РЕЗУЛЬТАТ С {create_result}")

    read_result = await db_manager.bookings.get_one_or_none(id=create_result.id)
    assert read_result
    print(f"РЕЗУЛЬТАТ R {read_result}")


    update_date_to = date_to=date(year=2025, month=12, day=7)
    update_date = BookingSchemaAddRequest(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=12, day=5),
        date_to=update_date_to,
        price=100
    )
    await db_manager.bookings.edit(update_data=update_date, exclude_unset=True, id=create_result.id)
    update_result =await db_manager.bookings.get_one_or_none(id=create_result.id)
    assert update_result
    assert update_result.date_to == update_date_to
    print(f"РЕЗУЛЬТАТ U {update_result}")

    await db_manager.bookings.delete(id=create_result.id)
    delete_result = await db_manager.bookings.get_one_or_none(id=create_result.id)
    assert delete_result == None
    print(f"РЕЗУЛЬТАТ D {delete_result}")
    await db_manager.commit()