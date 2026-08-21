import pytest
import allure
from data import INVALID_INGREDIENT


@allure.suite("Создание заказа")
class TestCreateOrder:

    # ==========================================
    # СЦЕНАРИЙ: С авторизацией / С ингредиентами
    # ==========================================

    @allure.title("Авторизованный пользователь: проверка статус-кода 200")
    def test_create_order_authorized_status_code(self, authorized_order_response):
        assert authorized_order_response.status_code == 200

    @allure.title("Авторизованный пользователь: проверка поля success в ответе")
    def test_create_order_authorized_success_field(self, authorized_order_response):
        assert authorized_order_response.json().get("success") is True

    @allure.title("Авторизованный пользователь: проверка наличия имени бургера")
    def test_create_order_authorized_has_name(self, authorized_order_response):
        assert "name" in authorized_order_response.json()

    @allure.title("Авторизованный пользователь: проверка генерации номера заказа")
    def test_create_order_authorized_has_order_number(self, authorized_order_response):
        assert "number" in authorized_order_response.json().get("order", {})

    # ==========================================
    # СЦЕНАРИЙ: Без авторизации
    # ==========================================

    @allure.title("Неавторизованный пользователь: проверка статус-кода")
    def test_create_order_unauthorized_status_code(self, unauthorized_order_response):
        assert unauthorized_order_response.status_code == 200

    @allure.title("Неавторизованный пользователь: проверка поля success в ответе")
    def test_create_order_unauthorized_success_field(self, unauthorized_order_response):
        assert unauthorized_order_response.json().get("success") is True

    @allure.title("Неавторизованный пользователь: проверка генерации номера заказа")
    def test_create_order_unauthorized_has_order_number(self, unauthorized_order_response):
        assert "number" in unauthorized_order_response.json().get("order", {})

    # ==========================================
    # СЦЕНАРИЙ: Без ингредиентов
    # ==========================================

    @allure.title("Создание заказа без ингредиентов: проверка статус-кода 400")
    def test_create_order_no_ingredients_status_code(self, no_ingredients_order_response):
        assert no_ingredients_order_response.status_code == 400

    @allure.title("Создание заказа без ингредиентов: проверка тела ответа")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "Ingredient ids must be provided")
    ])
    def test_create_order_no_ingredients_body_fields(self, no_ingredients_order_response, json_key, expected_value):
        assert no_ingredients_order_response.json().get(json_key) == expected_value

    # ==========================================
    # СЦЕНАРИЙ: С неверным хешем ингредиентов
    # ==========================================

    @allure.title("Создание заказа с неверным хешем: проверка статус-кода 500")
    def test_create_order_invalid_hash_status_code(self, invalid_hash_order_response):
        assert invalid_hash_order_response.status_code == 500
