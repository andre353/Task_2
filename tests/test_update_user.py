import pytest
import allure
from helpers import generate_random_string


@allure.suite("Изменение данных пользователя")
class TestUpdateUser:

    # ==========================================
    # СЦЕНАРИЙ: С авторизацией
    # ==========================================

    @allure.title("Изменение данных авторизованным пользователем: проверка статус-кода 200")
    @pytest.mark.parametrize("update_user_authorized_response", [
        ("email", f"new_email_{generate_random_string(5)}@yandex.ru"),
        ("name", f"NewName_{generate_random_string(5)}"),
        ("password", generate_random_string(12))
    ], indirect=True)
    def test_update_user_authorized_status_code(self, update_user_authorized_response):
        response, _, _ = update_user_authorized_response
        assert response.status_code == 200

    @allure.title("Изменение данных авторизованным пользователем: проверка поля success")
    @pytest.mark.parametrize("update_user_authorized_response", [
        ("email", f"new_email_{generate_random_string(5)}@yandex.ru"),
        ("name", f"NewName_{generate_random_string(5)}"),
        ("password", generate_random_string(12))
    ], indirect=True)
    def test_update_user_authorized_success_field(self, update_user_authorized_response):
        response, _, _ = update_user_authorized_response
        assert response.json().get("success") is True

    @allure.title("Изменение данных авторизованным пользователем: проверка обновленного значения")
    @pytest.mark.parametrize("update_user_authorized_response", [
        ("email", f"new_email_{generate_random_string(5)}@yandex.ru"),
        ("name", f"NewName_{generate_random_string(5)}")
    ], indirect=True)
    def test_update_user_authorized_value_updated(self, update_user_authorized_response):
        response, field_to_update, expected_value = update_user_authorized_response        
        assert response.json().get("user", {}).get(field_to_update) == expected_value

    # ==========================================
    # СЦЕНАРИЙ: Без авторизации
    # ==========================================

    @allure.title("Попытка изменения данных неавторизованным пользователем: проверка поля success")
    @pytest.mark.parametrize("update_user_unauthorized_response", [
        ("email", "unauth_email@yandex.ru"),
        ("name", "UnauthName"),
        ("password", "UnauthPassword123")
    ], indirect=True)
    def test_update_user_data_unauthorized_success_field(self, update_user_unauthorized_response):
        assert update_user_unauthorized_response.json().get("success") is False

    @allure.title("Попытка изменения данных неавторизованным пользователем: проверка сообщения об ошибке")
    @pytest.mark.parametrize("update_user_unauthorized_response", [
        ("email", "unauth_email@yandex.ru"),
        ("name", "UnauthName"),
        ("password", "UnauthPassword123")
    ], indirect=True)
    def test_update_user_data_unauthorized_message(self, update_user_unauthorized_response):
        assert update_user_unauthorized_response.json().get("message") == "You should be authorised"
