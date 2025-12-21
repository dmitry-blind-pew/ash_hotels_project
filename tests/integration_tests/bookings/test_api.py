import pytest

from tests.conftest import get_db_manager_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-12-05", "2025-12-06", 200),
        (1, "2025-12-05", "2025-12-06", 200),
        (1, "2025-12-05", "2025-12-06", 200),
        (1, "2025-12-05", "2025-12-06", 200),
        (1, "2025-12-05", "2025-12-06", 200),
        (1, "2025-12-05", "2025-12-06", 409),
        (1, "2025-12-08", "2025-12-09", 200),
    ],
)
async def test_create_booking(auth_async_client, room_id, date_from, date_to, status_code):
    response = await auth_async_client.post(
        "/bookings", json={"room_id": room_id, "date_from": date_from, "date_to": date_to}
    )
    json_data = response.json()

    assert response.status_code == status_code
    if status_code == 200:
        assert isinstance(json_data, dict)
        assert json_data["status"] == "Booking added"
        assert json_data["data"]


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for dbnp in get_db_manager_null_pool():
        await dbnp.bookings.delete()
        await dbnp.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, count_bookings",
    [
        (1, "2025-12-05", "2025-12-06", 200, 1),
        (1, "2025-12-05", "2025-12-06", 200, 2),
        (1, "2025-12-05", "2025-12-06", 200, 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, status_code, count_bookings, delete_all_bookings, auth_async_client
):
    response = await auth_async_client.post(
        "/bookings", json={"room_id": room_id, "date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == status_code
    response = await auth_async_client.get("/bookings/me")
    assert response.status_code == status_code
    assert len(response.json()) == count_bookings
