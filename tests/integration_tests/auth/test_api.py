import pytest
from fastapi import HTTPException


@pytest.mark.parametrize("email, password, status_code", [
    ("test@rambler.ru", "qwerty", 200),
    ("test@email.com", "1234", 200),
    ("", "1234", 422),
    ("testyandex.ru", "1234", 422)
])
async def test_auth_reg_login_me_logout(email, password, status_code, async_client, setup_database):
    register_user = await async_client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )

    assert register_user.status_code == status_code
    if status_code != 200:
        return

    login_user = await async_client.post(
        "/auth/login",
        json={"email": email, "password": password}
    )
    assert login_user.status_code == status_code
    user_token = login_user.cookies["access_token"]
    assert user_token is not None

    user_me = await async_client.get("/auth/me")
    user_me_dict = user_me.json()
    assert user_me.status_code == status_code
    assert user_me_dict["email"] == email

    logout_user = await async_client.post("/auth/logout")
    assert logout_user.status_code == status_code
    try:
        none_user = await async_client.get("/auth/me")
    except HTTPException(422):
        assert none_user.status_code == 422



