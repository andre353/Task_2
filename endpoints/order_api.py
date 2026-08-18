import requests
import allure
from urls import ORDERS


class OrderApi:
    def __init__(self, base_url):
        self.base_url = base_url

    @allure.step("Отправка запроса на создание заказа")
    def create_order(self, payload, headers=None):
        """
        Выполняет POST-запрос к API создания заказа.
        headers передаются опционально для тестов с авторизацией/без авторизации.
        """
        response = requests.post(f"{self.base_url}{ORDERS}", json=payload, headers=headers)
        return response

    
