import allure
import requests
import time
from data import Data

@allure.feature("User Data API")
class TestUserDataAPI:
    import time

    @allure.story("Update User Data with Auth")
    def test_update_user_data_with_auth(self, auth_token):
        headers = {"Authorization": f"{auth_token}"}
        unique_email = f"updated_user_{int(time.time())}@example.com"
        payload = {
            "email": unique_email,
            "name": "Updated Name"
        }
        print(f"Headers: {headers}")  # Отладочный вывод
        print(f"Payload: {payload}")  # Отладочный вывод
        response = requests.patch(f"{Data.BASE_URL}/auth/user", headers=headers, json=payload)
        print(f"Response status code: {response.status_code}")  # Отладочный вывод
        print(f"Response body: {response.json()}")  # Отладочный вывод
        assert response.status_code == 200, f"Expected status code 200 for authorized update, but got {response.status_code}: {response.text}"
        assert response.json()["user"]["email"] == unique_email, "Email should be updated"

    @allure.story("Update User Data without Auth")
    def test_update_user_data_without_auth(self):
        payload = {
            "email": "updated_user@example.com",
            "name": "Updated Name"
        }
        response = requests.patch(f"{Data.BASE_URL}/auth/user", json=payload)
        assert response.status_code == 401, "Expected status code 401 for unauthorized update"
        assert response.json()["message"] == "You should be authorised", "Incorrect error message"