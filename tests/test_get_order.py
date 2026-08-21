import pytest
import allure


@allure.suite("Получение заказов пользователя")
class TestGetOrders:

    # ==========================================
    # СЦЕНАРИЙ: Авторизованный пользователь
    # ==========================================

    @allure.title("Авторизованный пользователь: проверка статус-кода 200")
    def test_get_orders_authorized_status_code(self, user_orders_response):
        assert user_orders_response.status_code == 200

    @allure.title("Авторизованный пользователь: проверка поля success в ответе")
    def test_get_orders_authorized_success_field(self, user_orders_response):
        assert user_orders_response.json().get("success") is True

    @allure.title("Авторизованный пользователь: проверка наличия ключа orders в теле")
    def test_get_orders_authorized_has_orders_key(self, user_orders_response):
        assert "orders" in user_orders_response.json()

    @allure.title("Авторизованный пользователь: проверка, что orders является списком")
    def test_get_orders_authorized_orders_is_list(self, user_orders_response):
        assert isinstance(user_orders_response.json().get("orders"), list)

    # ==========================================
    # СЦЕНАРИЙ: Неавторизованный пользователь
    # ==========================================

# --- СЦЕНАРИЙ: Неавторизованный пользователь ---

    @allure.title("Неавторизованный пользователь: проверка статус-кода 401")
    def test_get_orders_unauthorized_status_code(self, unauthorized_orders_response):
        assert unauthorized_orders_response.status_code == 401

    @allure.title("Неавторизованный пользователь: проверка полей тела ответа")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "You should be authorised")
    ])
    def test_get_orders_unauthorized_body_fields(self, unauthorized_orders_response, json_key, expected_value):
        assert unauthorized_orders_response.json().get(json_key) == expected_value

