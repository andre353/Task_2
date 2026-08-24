import pytest
import allure
from helpers import generate_user_payload


@allure.suite("Создание пользователя")
class TestCreateUser:
    # ==========================================
    # СЦЕНАРИЙ: создать уникального пользователя
    # ==========================================
    @allure.title("Создание уникального пользователя: проверка статус-кода")
    def test_create_unique_user_status_code(self, user_api, cleanup_user):
        payload = generate_user_payload()        
        response = user_api.register_user(payload)
        cleanup_user["response"] = response 

        assert response.status_code == 200

    @allure.title("Создание уникального пользователя: проверка наличия токена")
    def test_create_unique_user_has_token(self, user_api, cleanup_user):
        payload = generate_user_payload()        
        response = user_api.register_user(payload)
        cleanup_user["response"] = response 

        assert "accessToken" in response.json()

    # ==========================================
    # СЦЕНАРИЙ: создать пользователя, который уже зарегистрирован
    # ==========================================           

    @allure.title("Создание дубликата: проверка статус-кода 403")
    def test_create_duplicate_user_status_code(self, user_api, cleanup_user):
        duplicate_payload = generate_user_payload()
        
        first_response = user_api.register_user(duplicate_payload)
        cleanup_user["response"] = first_response

        second_response = user_api.register_user(duplicate_payload)
        
        assert second_response.status_code == 403       

    @allure.title("Создание дубликата: проверка сообщения об ошибке")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "User already exists")
    ])
    def test_create_duplicate_user_body_fields(self, user_api, cleanup_user, json_key, expected_value):
        duplicate_payload = generate_user_payload()
        
        first_response = user_api.register_user(duplicate_payload)
        cleanup_user["response"] = first_response

        second_response = user_api.register_user(duplicate_payload)
        
        assert second_response.json().get(json_key) == expected_value       

    # ==========================================
    # СЦЕНАРИЙ: создать пользователя и не заполнить одно из обязательных полей
    # ==========================================     

    @allure.title("Создание пользователя без обязательного поля: проверка статус-кода 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_status_code(self, user_api, missing_field):
        payload = generate_user_payload()
        payload.pop(missing_field) # Удаляем обязательное поле из словаря перед отправкой        
        response = user_api.register_user(payload)
                
        assert response.status_code == 403

    @allure.title("Создание пользователя без обязательного поля: проверка тела ответа")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "Email, password and name are required fields")
    ])
    def test_create_user_missing_field_body_fields(self, user_api, missing_field, json_key, expected_value):
        payload = generate_user_payload()
        payload.pop(missing_field)        
        response = user_api.register_user(payload)
        
        assert response.json().get(json_key) == expected_value
