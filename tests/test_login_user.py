import pytest
import allure


@allure.suite("Логин пользователя")
class TestLoginUser:

    # ==========================================
    # СЦЕНАРИЙ: логин под существующим пользователем
    # ==========================================

    @allure.title("Логин под существующим пользователем: проверка статус-кода")
    def test_login_success_status_code(self, user_api, auth_user):
        login_payload = {
            "email": auth_user["user_data"]["email"],
            "password": auth_user["user_data"]["password"]
        }
        response = user_api.login_user(login_payload)

        assert response.status_code == 200

    @allure.title("Логин под существующим пользователем: проверка поля success")
    def test_login_success_field(self, user_api, auth_user):
        login_payload = {
            "email": auth_user["user_data"]["email"],
            "password": auth_user["user_data"]["password"]
        }
        response = user_api.login_user(login_payload)

        assert response.json().get("success") is True

    @allure.title("Логин под существующим пользователем: проверка токена в ответе")
    def test_login_success_has_token(self, user_api, auth_user):
        login_payload = {
            "email": auth_user["user_data"]["email"],
            "password": auth_user["user_data"]["password"]
        }
        response = user_api.login_user(login_payload)

        assert "accessToken" in response.json()

    # ==========================================
    # СЦЕНАРИЙ: логин с неверным логином и паролем
    # ==========================================

    @allure.title("Логин с неверным паролем: проверка статус-кода")
    def test_login_wrong_credentials_status_code(self, user_api, auth_user):
        login_payload = {
            "email": auth_user["user_data"]["email"],
            "password": "wrong_password_123"
        }
        response = user_api.login_user(login_payload)

        assert response.status_code == 401

    @allure.title("Логин с неверным логином и паролем: проверка сообщения об ошибке")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "email or password are incorrect")
    ])
    def test_login_wrong_credentials_body_fields(self, user_api, auth_user, json_key, expected_value):
        login_payload = {
            "email": auth_user["user_data"]["email"],
            "password": "wrong_password_123"
        }    
        response = user_api.login_user(login_payload)    

        assert response.json().get(json_key) == expected_value
