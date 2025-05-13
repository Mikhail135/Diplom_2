import allure
import requests
from data import Data
import time

@allure.title("User API")
class TestUserAPI:

    @allure.title("Create Unique User")
    def test_create_unique_user(self):
        unique_email = f"unique_user_{int(time.time())}@example.com"  # Генерация уникального email
        payload = {
            "email": unique_email,
            "password": "password123",
            "name": "Unique User"
        }
        response = requests.post(f"{Data.BASE_URL}/auth/register", json=payload)
        assert response.status_code == 200, "Expected status code 200 for unique user"
        assert response.json()["success"], "Response should indicate success"

    @allure.title("Create Existing User")
    def test_create_existing_user(self):
        payload = {
            "email": "existing_user@example.com",
            "password": "password123",
            "name": "Existing User"
        }
        response = requests.post(f"{Data.BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403, "Expected status code 403 for existing user"
        assert response.json()["message"] == "User already exists", "Incorrect error message"

    @allure.title("Create User with Missing Fields")
    def test_create_user_with_missing_fields(self):
        payload = {
            "email": "incomplete_user@example.com"
        }
        response = requests.post(f"{Data.BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403, "Expected status code 403 for missing fields"
        assert response.json()["message"] == "Email, password and name are required fields", "Incorrect error message"

    @allure.title("Login with Valid Credentials")
    def test_login_with_valid_credentials(self):
        payload = {
            "email": "existing_user@example.com",
            "password": "password123"
        }
        response = requests.post(f"{Data.BASE_URL}/auth/login", json=payload)
        assert response.status_code == 200, "Expected status code 200 for valid credentials"
        assert response.json()["success"], "Response should indicate success"

    @allure.title("Login with Invalid Credentials")
    def test_login_with_invalid_credentials(self):
        payload = {
            "email": "nonexistent@example.com",
            "password": "wrong_password"
        }
        response = requests.post(f"{Data.BASE_URL}/auth/login", json=payload)
        assert response.status_code == 401, "Expected status code 401 for invalid credentials"
        assert response.json()["message"] == "email or password are incorrect", "Incorrect error message"