import allure
import requests
from data import Data


@allure.feature("Orders API")
class TestOrdersAPI:
    @allure.story("Create Order with Auth")
    def test_create_order_with_auth(self, auth_token):
        headers = {"Authorization": f"{auth_token}"}
        payload = {
        "ingredients": ["61c0c5a71d1f82001bdaaa6c","61c0c5a71d1f82001bdaaa6d"]
        }
        response = requests.post(f"{Data.BASE_URL}/orders", headers=headers, json=payload)
        assert response.status_code == 200, "Expected status code 200 for order creation"
        assert "order" in response.json(), "Response should contain 'order' field"

    @allure.story("Create Order without Ingredients")
    def test_create_order_without_ingredients(self, auth_token):
        headers = {"Authorization": f"{auth_token}"}
        response = requests.post(f"{Data.BASE_URL}/orders", headers=headers, json={})
        assert response.status_code == 400, "Expected status code 400 for missing ingredients"
        assert response.json()["message"] == "Ingredient ids must be provided", "Incorrect error message"

    @allure.story("Get User Orders with Auth")
    def test_get_user_orders_with_auth(self, auth_token):
        headers = {"Authorization": f"{auth_token}"}
        response = requests.get(f"{Data.BASE_URL}/orders", headers=headers)
        assert response.status_code == 200, "Expected status code 200 for fetching orders"
        assert "orders" in response.json(), "Response should contain 'orders' field"

    @allure.story("Get User Orders without Auth")
    def test_get_user_orders_without_auth(self):
        response = requests.get(f"{Data.BASE_URL}/orders")
        assert response.status_code == 401, "Expected status code 401 for unauthorized access"
        assert response.json()["message"] == "You should be authorised", "Incorrect error message"

