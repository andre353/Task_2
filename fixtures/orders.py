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


