import random
from helpers import generate_random_string


# Данные для параметризации тестов булочки (Bun)
BUN_NAMES = ["Краторная булка N-200i", "Флюоресцентная булка R2-D3"]
BUN_PRICES = [1255, 988]

# Данные для параметризации тестов соусов (Sauce)
SAUCE_NAMES = [
    "Соус с шипами Антарианского плоскоходца", 
    "Соус Spicy-X", 
    "Соус фирменный Space Sauce", 
    "Соус традиционный галактический"
]
SAUCE_PRICES = [88, 90, 80, 15]

# Данные для параметризации тестов начинки (Ingredient/Filling)
FILLING_NAMES = [
    "Хрустящие минеральные кольца", 
    "Плоды Фалленианского дерева", 
    "Кристаллы марсианских альфа-сахаридов", 
    "Мини-салат Экзо-Плантаго", 
    "Сыр с астероидной плесенью", 
    "Филе Люминесцентного тетраодонтимформа"
]
FILLING_PRICES = [300, 874, 762, 4400, 4142, 988]

# Валидные хеши ингредиентов со скриншота задания
VALID_INGREDIENTS = ["60d3b41abdacab0026a733c6", "60d3b41abdacab0026a733c7"]
INVALID_INGREDIENT = "60d3b41abdacab0026a733cZ" 



def get_order_response_data():
    """Возвращает макет успешного ответа сервера для проверок (mock/expected data)."""
    return {
        "name": f"Краторный метеоритный бургер_{generate_random_string(3)}",
        "order": {
            "number": random.randint(1000, 9999)
        },
        "success": True
    }


def get_order_body_data(ingredients_list=None): 
    """
    Возвращает тело запроса для создания заказа.
    Если список не передан, использует валидные ингредиенты.
    """
    if ingredients_list is None:
        ingredients_list = VALID_INGREDIENTS
    return {
        "ingredients": ingredients_list
    }
