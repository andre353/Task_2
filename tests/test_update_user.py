import pytest
import allure
from helpers import generate_random_string


@allure.suite("Изменение данных пользователя")
class TestUpdateUser:

    # ==========================================
    # СЦЕНАРИЙ: С авторизацией
    # ==========================================
    
    @allure.title("Изменение данных авторизованным пользователем: проверка статус-кода 200")
    @pytest.mark.parametrize("field_to_update, new_value", [
        ("email", f"new_email_{generate_random_string(5)}@yandex.ru"),
        ("name", f"NewName_{generate_random_string(5)}"),
        ("password", generate_random_string(12))
    ])
    def test_update_user_authorized_status_code(self, user_api, auth_user, field_to_update, new_value):
        headers = {"Authorization": auth_user["token"]}
        payload = {field_to_update: new_value}        
        response = user_api.update_user_data(payload=payload, headers=headers)
        
        assert response.status_code == 200

    @allure.title("Изменение данных авторизованным пользователем: проверка поля success")
    @pytest.mark.parametrize("field_to_update, new_value", [
        ("email", f"new_email_{generate_random_string(5)}@yandex.ru"),
        ("name", f"NewName_{generate_random_string(5)}"),
        ("password", generate_random_string(12))
    ])
    def test_update_user_authorized_success_field(self, user_api, auth_user, field_to_update, new_value):
        headers = {"Authorization": auth_user["token"]}
        payload = {field_to_update: new_value}        
        response = user_api.update_user_data(payload=payload, headers=headers)
        
        assert response.json().get("success") is True

    @allure.title("Изменение данных авторизованным пользователем: проверка обновленного значения")
    @pytest.mark.parametrize("field_to_update, new_value", [
        ("email", f"new_email_{generate_random_string(5)}@yandex.ru"),
        ("name", f"NewName_{generate_random_string(5)}")
    ])
    def test_update_user_authorized_value_updated(self, user_api, auth_user, field_to_update, new_value):
        headers = {"Authorization": auth_user["token"]}
        payload = {field_to_update: new_value}        
        response = user_api.update_user_data(payload, headers=headers)
        
        assert response.json().get("user", {}).get(field_to_update) == new_value

    # ==========================================
    # СЦЕНАРИЙ: Без авторизации
    # ==========================================

    @allure.title("Попытка изменения данных неавторизованным пользователем: проверка поля success")
    @pytest.mark.parametrize("field_to_update, new_value", [
        ("email", "unauth_email@yandex.ru"),
        ("name", "UnauthName"),
        ("password", "UnauthPassword123")
    ])
    def test_update_user_unauthorized_success_field(self, user_api, field_to_update, new_value):
        headers = {"Authorization": ""} 
        payload = {field_to_update: new_value}        
        response = user_api.update_user_data(payload=payload, headers=headers)
        
        assert response.json().get("success") is False

    @allure.title("Попытка изменения данных неавторизованным пользователем: проверка сообщения об ошибке")
    @pytest.mark.parametrize("field_to_update, new_value", [
        ("email", "unauth_email@yandex.ru"),
        ("name", "UnauthName"),
        ("password", "UnauthPassword123")
    ])
    def test_update_user_unauthorized_message(self, user_api, field_to_update, new_value):
        headers = {"Authorization": ""}
        payload = {field_to_update: new_value}        
        response = user_api.update_user_data(payload=payload, headers=headers)
        
        assert response.json().get("message") == "You should be authorised"
