import random
import string


def generate_random_string(length=10):
    """Генерирует случайную строку из строчных латинских букв."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))

def generate_user_payload():
    """
    Генерирует валидные данные для регистрации нового пользователя (/api/auth/register).
    """
    return {
        "email": f"test_{generate_random_string(8)}@yandex.ru",
        "password": generate_random_string(10),
        "name": f"User_{generate_random_string(5)}"
    }

def generate_order_payload(ingredients_list=None):
    """
    Формирует тело запроса для создания заказа с ингредиентами (/api/orders).
    Если список не передан, возвращает пустой список для негативных тестов.
    """
    if ingredients_list is None:
        ingredients_list = []
        
    return {
        "ingredients": ingredients_list
    }    