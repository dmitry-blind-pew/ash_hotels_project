from src.services.auth import AuthService


def test_create_and_decode_access_token():
    data = {"user_id": 1}
    encoded_jwt = AuthService().create_access_token(data)

    decoded_jwt = AuthService().decode_access_token(encoded_jwt)

    assert decoded_jwt
    assert decoded_jwt["user_id"] == data["user_id"]
