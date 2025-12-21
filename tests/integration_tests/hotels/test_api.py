async def test_hotels_get(async_client):
    response = await async_client.get("/hotels", params={"date_from": "2025-12-05", "date_to": "2025-12-06"})
    print(f"GET HOTELS TEST: {response.json()}")
    assert response.status_code == 200
