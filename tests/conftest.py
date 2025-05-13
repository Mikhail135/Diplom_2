import time
import pytest
import requests
from data import Data
import logging

logging.basicConfig(level=logging.INFO)
@pytest.fixture(scope="function")
def create_user():
    """Фикстура для создания уникального пользователя."""
    email = f"unique_user_{int(time.time())}@example.com"
    password = "password123"
    name = "Unique User"
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    register_response = requests.post(f"{Data.BASE_URL}/auth/register", json=payload)
    if register_response.status_code != 200:
        logging.error(f"Failed to create user: {register_response.text}")
        yield None

    # Авторизуемся для получения токена
    login_payload = {"email": email, "password": password}
    login_response = requests.post(f"{Data.BASE_URL}/auth/login", json=login_payload)
    if login_response.status_code != 200:
        logging.error(f"Failed to login: {login_response.text}")
        yield None

    token = login_response.json().get("accessToken")
    if not token:
        logging.error("Access token is missing in the login response")
        yield
    yield {"email": email, "password": password, "name": name, "token": token}
    delete_headers = {"Authorization": f"Bearer {token}"}
    delete_response = requests.delete(f"{Data.BASE_URL}/auth/user", headers=delete_headers)
    if delete_response.status_code != 200:
        logging.error(f"Failed to delete user: {delete_response.text}")

@pytest.fixture(scope="function")
def auth_token(create_user):
    email = create_user["email"]
    password = create_user["password"]
    payload = {"email": email, "password": password}
    response = requests.post(f"{Data.BASE_URL}/auth/login", json=payload)
    token = response.json()["accessToken"]
    return token