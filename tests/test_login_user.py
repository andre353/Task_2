import pytest
import allure


@allure.suite("Логин пользователя")
class TestLoginUser:

    # ==========================================
    # СЦЕНАРИЙ: логин под существующим пользователем
    # ==========================================

    @allure.title("Логин под существующим пользователем: проверка статус-кода 200")
    def test_login_success_status_code(self, successful_login_response):
        assert successful_login_response.status_code == 200

    @allure.title("Логин под существующим пользователем: проверка поля success")
    def test_login_success_field(self, successful_login_response):
        assert successful_login_response.json().get("success") is True

    @allure.title("Логин под существующим пользователем: проверка токена в ответе")
    def test_login_success_has_token(self, successful_login_response):
        assert "accessToken" in successful_login_response.json()

    # ==========================================
    # СЦЕНАРИЙ: логин с неверным логином и паролем
    # ==========================================    

    @allure.title("Логин с неверным паролем: проверка статус-кода 401")
    def test_login_wrong_credentials_status_code(self, invalid_credentials_login_response):
        assert invalid_credentials_login_response.status_code == 401

    @allure.title("Логин с неверным паролем: проверка сообщения об ошибке")
    @pytest.mark.parametrize("json_key, expected_value", [
        ("success", False),
        ("message", "email or password are incorrect")
    ])
    def test_login_wrong_credentials_body_fields(self, invalid_credentials_login_response, json_key, expected_value):
        assert invalid_credentials_login_response.json().get(json_key) == expected_value
