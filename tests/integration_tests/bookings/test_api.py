from datetime import date, timedelta


async def test_create_booking(db_manager, auth_async_client):
    room_id = (await db_manager.rooms.get_all())[0].id
    response = await auth_async_client.post(
        "/bookings",
        json = {
            "room_id": room_id,
            "date_from": "2025-12-05",
            "date_to": "2025-12-06"
        }
    )
    json_data = response.json()

    assert response.status_code == 200
    assert isinstance(json_data, dict)
    assert json_data["status"] == "Booking added"
    assert json_data["data"]