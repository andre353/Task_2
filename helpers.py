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