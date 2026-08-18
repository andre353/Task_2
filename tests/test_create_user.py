import pytest
import allure
from helpers import generate_user_payload


@allure.suite("Создание пользователя")
class TestCreateUser:

    # ==========================================
    # СЦЕНАРИЙ: создать уникального пользователя
    # ==========================================

    @allure.title("Создание уникального пользователя: проверка статус-кода")
    def test_create_unique_user_status_code(self, user_api):
        payload = generate_user_payload()
        response = user_api.register_user(payload)
        token = response.json().get("accessToken")
        try:
            assert response.status_code == 200
        finally:
            if token:
                user_api.delete_user(headers={"Authorization": token})

    @allure.title("Создание уникального пользователя: проверка наличия токена")
    def test_create_unique_user_has_token(self, user_api):
        payload = generate_user_payload()
        response = user_api.register_user(payload)
        token = response.json().get("accessToken")
        try:
            assert "accessToken" in response.json()
        finally:
            if token:
                user_api.delete_user(headers={"Authorization": token})

    # ==========================================
    # СЦЕНАРИЙ: создать пользователя, который уже зарегистрирован
    # ==========================================            

    @allure.title("Создание дубликата: проверка статус-кода 403")
    def test_create_duplicate_user_status_code(self, user_api, auth_user):
        duplicate_payload = auth_user["user_data"]
        response = user_api.register_user(duplicate_payload)
        assert response.status_code == 403

    @allure.title("Создание дубликата: проверка сообщения об ошибке")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "User already exists")
    ])
    def test_create_duplicate_user_body_fields(self, user_api, auth_user, json_key, expected_value):
        duplicate_payload = auth_user["user_data"]
        response = user_api.register_user(duplicate_payload)
        assert response.json().get(json_key) == expected_value

    # ==========================================
    # СЦЕНАРИЙ: создать пользователя и не заполнить одно из обязательных полей
    # ==========================================     

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_error(self, user_api, missing_field):
        payload = generate_user_payload()
        payload.pop(missing_field)
        
        response = user_api.register_user(payload)
        response_json = response.json()
        
        # Проверяем структуру одной строкой, так как это неделимая логика ошибки
        assert response.status_code == 403 and response_json.get("success") is False and response_json.get("message") == "Email, password and name are required fields"
