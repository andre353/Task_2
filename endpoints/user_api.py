import requests
import allure
from urls import USER_REGISTER, USER_LOGIN, USER_DATA


class UserApi:
    def __init__(self, base_url):
        self.base_url = base_url

    @allure.step("Регистрация нового пользователя")
    def register_user(self, payload):
        return requests.post(f"{self.base_url}{USER_REGISTER}", json=payload)

    @allure.step("Авторизация пользователя")
    def login_user(self, payload):
        return requests.post(f"{self.base_url}{USER_LOGIN}", json=payload)

    @allure.step("Удаление пользователя")
    def delete_user(self, headers):
        return requests.delete(f"{self.base_url}{USER_DATA}", headers=headers)

    @allure.step("Изменение данных пользователя")
    def update_user_data(self, payload, headers):
        return requests.patch(f"{self.base_url}{USER_DATA}", json=payload, headers=headers)
