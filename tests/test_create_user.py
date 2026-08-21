import pytest
import allure
from helpers import generate_user_payload


@allure.suite("Создание пользователя")
class TestCreateUser:

    # ==========================================
    # СЦЕНАРИЙ: создать уникального пользователя
    # ==========================================

    @allure.title("Создание уникального пользователя: проверка статус-кода")
    def test_create_unique_user_status_code(self, user_api, auth_user_response):
        assert auth_user_response.status_code == 200

    @allure.title("Создание уникального пользователя: проверка наличия токена")
    def test_create_unique_user_has_token(self, user_api, auth_user_response):
        assert "accessToken" in auth_user_response.json()

    # ==========================================
    # СЦЕНАРИЙ: создать пользователя, который уже зарегистрирован
    # ==========================================            

    @allure.title("Создание дубликата: проверка статус-кода 403")
    def test_create_duplicate_user_status_code(self, duplicate_user_response):
        assert duplicate_user_response.status_code == 403

    @allure.title("Создание дубликата: проверка сообщения об ошибке")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "User already exists")
    ])
    def test_create_duplicate_user_body_fields(self, duplicate_user_response, json_key, expected_value):
        assert duplicate_user_response.json().get(json_key) == expected_value

    # ==========================================
    # СЦЕНАРИЙ: создать пользователя и не заполнить одно из обязательных полей
    # ==========================================     

    @allure.title("Создание пользователя без обязательного поля: проверка статус-кода 403")
    # Передаем параметры через indirect=True прямо в фикстуру запроса
    @pytest.mark.parametrize("missing_field_user_response", ["email", "password", "name"], indirect=True)
    def test_create_user_missing_field_status_code(self, missing_field_user_response):
        assert missing_field_user_response.status_code == 403

    @allure.title("Создание пользователя без обязательного поля: проверка тела ответа")
    @pytest.mark.parametrize("missing_field_user_response", ["email", "password", "name"], indirect=True)
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "Email, password and name are required fields")
    ])
    def test_create_user_missing_field_body_fields(self, missing_field_user_response, json_key, expected_value):
        assert missing_field_user_response.json().get(json_key) == expected_value
