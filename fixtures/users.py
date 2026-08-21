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
    Регистрирует пользователя перед тестом.
    Возвращает кортеж (response, payload).
    После теста гарантированно удаляет пользователя.
    """
    payload = generate_user_payload()
    response = user_api.register_user(payload)    
    # Передаем в тест и ответ сервера, и те данные, что отправляли
    yield response, payload    
    # Очистка данных (Teardown)
    try:
        token = response.json().get("accessToken")
        if token:
            user_api.delete_user(headers={"Authorization": token})
    except Exception:
        pass # Защита на случай, если response.json() упал с ошибкой

@pytest.fixture
def auth_user_response(auth_user):
    """Возвращает объект ответа Response для проверки результатов регистрации."""
    auth_response, _ = auth_user
    return auth_response

@pytest.fixture
def auth_token(auth_user):
    """Возвращает СТРОКУ токена для авторизации в других ручках."""
    auth_response, _ = auth_user
    return auth_response.json().get("accessToken")

@pytest.fixture
def auth_user_payload(auth_user):
    """Извлекает чистый словарь с данными (payload) зарегистрированного пользователя."""
    _, payload = auth_user
    return payload

@pytest.fixture
def successful_login_response(user_api, auth_user_payload):
    """Выполняет запрос на авторизацию существующего пользователя с верными credentials."""
    login_data = {
        "email": auth_user_payload["email"],
        "password": auth_user_payload["password"]
    }
    return user_api.login_user(login_data)

@pytest.fixture
def invalid_credentials_login_response(user_api, auth_user_payload):
    """Выполняет запрос на авторизацию с валидным email, но неверным паролем."""
    login_data = {
        "email": auth_user_payload["email"],
        "password": "wrong_password_123"
    }
    return user_api.login_user(login_data)

@pytest.fixture
def update_user_authorized_response(user_api, auth_token, request):
    """
    Выполняет запрос на изменение данных авторизованного пользователя.
    Возвращает кортеж: (response, field_to_update, new_value)
    """
    field_to_update, new_value = request.param
    headers = {"Authorization": auth_token}
    payload = {field_to_update: new_value}
    
    response = user_api.update_user_data(payload=payload, headers=headers)
    
    yield response, field_to_update, new_value

@pytest.fixture
def update_user_unauthorized_response(user_api, request):
    """
    Выполняет запрос на изменение данных неавторизованного пользователя.
    Динамически принимает кортеж (field_to_update, new_value) через request.param.
    """
    field_to_update, new_value = request.param
    payload = {field_to_update: new_value}
    return user_api.update_user_data(payload=payload, headers=None)

