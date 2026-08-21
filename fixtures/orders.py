import pytest
import requests
from endpoints.order_api import OrderApi
from helpers import generate_user_payload
from urls import BASE_URL


@pytest.fixture(scope="session")
def order_api():
    return OrderApi(BASE_URL)

@pytest.fixture(scope="session")
def real_ingredients():
    """Динамически запрашивает актуальный список ингредиентов прямо со стенда."""
    try:
        response = requests.get(f"{BASE_URL}/ingredients")
        ingredients_data = response.json().get("data", [])
        # Берем ID первых двух продуктов из ответа сервера
        if len(ingredients_data) >= 2:
            return [ingredients_data[0]["_id"], ingredients_data[1]["_id"]]
    except Exception:
        pass
    
    # Резервный вариант, если сервер не ответил
    return ["60d3b41abdacab0026a733c6", "60d3b41abdacab0026a733c7"]

@pytest.fixture
def authorized_order_response(order_api, auth_token, real_ingredients):
    """Выполняет запрос на создание заказа с авторизацией и возвращает response."""
    headers = {"Authorization": auth_token}
    payload = {"ingredients": real_ingredients}
    return order_api.create_order(payload=payload, headers=headers)

@pytest.fixture
def unauthorized_order_response(order_api, real_ingredients):
    """Выполняет запрос на создание заказа БЕЗ авторизации и возвращает response."""
    payload = {"ingredients": real_ingredients}
    return order_api.create_order(payload=payload)    

@pytest.fixture
def no_ingredients_order_response(order_api, auth_token):
    """Выполняет запрос на создание заказа с пустым списком ингредиентов."""
    headers = {"Authorization": auth_token}
    payload = {"ingredients": []}
    return order_api.create_order(payload=payload, headers=headers)

@pytest.fixture
def invalid_hash_order_response(order_api, auth_token):
    """Выполняет запрос на создание заказа с неверным хешем ингредиентов."""
    headers = {"Authorization": auth_token}
    # INVALID_INGREDIENT должен передаваться как элемент списка []
    payload = {"ingredients": ["INVALID_INGREDIENT"]}
    return order_api.create_order(payload=payload, headers=headers)

@pytest.fixture
def user_orders_response(order_api, auth_token):
    """Выполняет GET-запрос на получение заказов авторизованного пользователя."""
    return order_api.get_user_orders(headers={"Authorization": auth_token})

@pytest.fixture
def unauthorized_orders_response(order_api):
    """Выполняет GET-запрос на получение заказов БЕЗ авторизации."""
    return order_api.get_user_orders(headers=None)

@pytest.fixture
def duplicate_user_response(user_api, auth_user_payload):
    """Выполняет запрос на создание дубликата пользователя."""
    return user_api.register_user(auth_user_payload)

@pytest.fixture
def missing_field_user_response(user_api, request):
    """
    Выполняет запрос на создание пользователя без одного из обязательных полей.
    Использует request.param для динамического получения пропущенного поля.
    """
    missing_field = request.param
    payload = generate_user_payload()
    payload.pop(missing_field)
    return user_api.register_user(payload)


