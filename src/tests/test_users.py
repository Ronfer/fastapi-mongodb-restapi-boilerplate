import pytest
import os

from jose import jwt
from httpx import AsyncClient
from dotenv import load_dotenv
from ..main import app
from ..models.auth_schemas import Token
from ..models.user_schemas import CreateUser
from fastapi.testclient import TestClient

load_dotenv()
client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.json().get('message') == 'Hello!'

# @pytest.mark.anyio
# async def test_create_user():
#     async with AsyncClient(app=app, base_url="/") as ac:
#         response = await ac.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})

#     new_user = CreateUser(response.json())
#     assert new_user.email == "hello123@gmail.com"
#     assert response.status_code == 201

# def test_login_user(test_user, client):
#     response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
#     login_response = Token(**response.json())
#     payload = jwt.decode(login_response.access_token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
#     id = payload.get("user_id")
#     assert id == test_user['id']
#     assert login_response.token_type == "bearer"
#     assert response.status_code == 200

# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'password123', 403),
#     ('sanjeev@gmail.com', 'wrongpassword', 403),
#     ('wrongemail@gmail.com', 'wrongpassword', 403),
#     (None, 'password123', 422),
#     ('sanjeev@gmail.com', None, 422)
# ])
# def test_incorrect_login(test_user, client, email, password, status_code):
#     response = client.post(
#         "/login", data={"username": email, "password": password})

#     assert response.status_code == status_code
    # assert response.json().get('detail') == 'Invalid Credentials'