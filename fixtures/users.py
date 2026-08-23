import pytest
from endpoints.user_api import UserApi
from helpers import generate_user_payload
from urls import BASE_URL


@pytest.fixture(scope="function")
def user_api():
    """Предоставляет объект класса UserApi для выполнения HTTP-запросов."""
    return UserApi(BASE_URL)

@pytest.fixture(scope="function")
def cleanup_user(user_api):
    """
    Универсальный инструмент очистки базы данных.
    Тест просто передает сюда объект response, а фикстура сама
    безопасно вытащит токен и удалит пользователя.
    """
    data = {"response": None}
    yield data
    
    response = data.get("response")
    if response:
        try:
            token = response.json().get("accessToken")
            if token:
                user_api.delete_user(headers={"Authorization": token})
        except Exception:
            pass

@pytest.fixture(scope="function")
def auth_user(user_api):
    payload = generate_user_payload()
    response = user_api.register_user(payload)
    
    token = None
    try:
        token = response.json().get("accessToken")
    except Exception:
        pass

    # Передаем словарь со всеми нужными данными в тесты
    user_info = {
        "response": response,
        "user_data": payload,
        "token": token
    }
    
    yield user_info
    
    if token:
        try:
            user_api.delete_user(headers={"Authorization": token})
        except Exception:
            pass

@pytest.fixture
def auth_token(auth_user):
    """
    Возвращает чистую строку токена.
    Используется в тестах, где сигнатура запрашивает напрямую auth_token.
    """
    return auth_user["token"]
