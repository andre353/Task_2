import pytest
import allure


@allure.suite("Получение заказов пользователя")
class TestGetOrders:

    # ==========================================
    # СЦЕНАРИЙ: Авторизованный пользователь
    # ==========================================

    @allure.title("Авторизованный пользователь: проверка статус-кода 200")
    def test_get_orders_authorized_status_code(self, order_api, auth_user):
        headers = {"Authorization": auth_user["token"]}
        response = order_api.get_user_orders(headers=headers)

        assert response.status_code == 200

    @allure.title("Авторизованный пользователь: проверка поля success в ответе")
    def test_get_orders_authorized_success_field(self, order_api, auth_user):
        headers = {"Authorization": auth_user["token"]}
        response = order_api.get_user_orders(headers=headers)

        assert response.json().get("success") is True

    @allure.title("Авторизованный пользователь: проверка наличия ключа orders в теле")
    def test_get_orders_authorized_has_orders_key(self, order_api, auth_user):
        headers = {"Authorization": auth_user["token"]}
        response = order_api.get_user_orders(headers=headers)

        assert "orders" in response.json()

    @allure.title("Авторизованный пользователь: проверка, что orders является списком")
    def test_get_orders_authorized_orders_is_list(self, order_api, auth_user):
        headers = {"Authorization": auth_user["token"]}
        response = order_api.get_user_orders(headers=headers)

        assert isinstance(response.json().get("orders"), list)

    # ==========================================
    # СЦЕНАРИЙ: Неавторизованный пользователь
    # ==========================================

    @allure.title("Неавторизованный пользователь: проверка статус-кода 401")
    def test_get_orders_unauthorized_status_code(self, order_api):
        response = order_api.get_user_orders(headers=None)

        assert response.status_code == 401

    @allure.title("Неавторизованный пользователь: проверка полей тела ответа")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "You should be authorised")
    ])
    def test_get_orders_unauthorized_body_fields(self, order_api, json_key, expected_value):
        response = order_api.get_user_orders(headers=None)

        assert response.json().get(json_key) == expected_value


