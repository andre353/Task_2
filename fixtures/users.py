import pytest
from endpoints.user_api import UserApi
from helpers import generate_user_payload
from urls import BASE_URL


@pytest.fixture(scope="function")
def user_api():
    """Предоставляет объект класса UserApi для выполнения HTTP-запросов."""
    return UserApi(BASE_URL)


@pytest.fixture(scope="function")
def auth_user(user_api):
    """
    Создает пользователя перед тестом, возвращает его данные и токен.
    После завершения теста удаляет пользователя из базы.
    """
    # Формируем email, password, name
    payload = generate_user_payload()
    
    # Регистрируем пользователя через класс UserApi
    response = user_api.register_user(payload) 
    response_data = response.json()
    token = response_data.get("accessToken")
    
    # Передаем данные в тест
    yield {
        "user_data": payload,
        "token": response_data.get("accessToken"),
        "refresh_token": response_data.get("refreshToken")
    }
    
    # Очистка данных после теста (TearDown)
    if token:
        user_api.delete_user(headers={"Authorization": token})
