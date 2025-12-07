

async def test_facilities_post(async_client):
    response_post = await async_client.post(
        '/facilities',
        json={"title": "wi-fi"}
    )
    assert response_post.status_code == 200
    print(f"TEST FACILITIES POST: {response_post.json()}")

async def test_facilities_get(async_client):
    response_get = await async_client.get('/facilities')
    assert response_get.status_code == 200
    print(f"TEST FACILITIES GET: {response_get.json()}")
