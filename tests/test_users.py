import pytest
from app.config import settings
from jose import jwt
from app.schemas.user import UserResponseSchema
from app.schemas.token import TokenSchema

def test_create_user(client):
    res = client.post("/users", json={"email": "hello123@gmail.com", "password": "password"})

    new_user = UserResponseSchema(**res.json())

    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user['password']})
    login_res = TokenSchema(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert test_user['id'] == id
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongEmail@gmail.com", "password", 403),
    ("hello123@gmail.com", "wrongPassword", 403),
    ("wrongEmail@gmail.com", "wrongPassword", 403),
    (None, "password", 422),
    ("hello123@gmail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code 


