from httpx import Client

from clients.authentication import get_authentication_client
from schemas.authentication import LoginRequestSchema


def build_private_client(user: LoginRequestSchema) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    :param user: Объект AuthenticationUserSchema с email и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """
    # Инициализируем AuthenticationClient для аутентификации
    authentication_client = get_authentication_client()

    payload = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.get_token(payload)

    return Client(
        timeout=90,
        base_url="http://localhost:8000",
        headers={"Authorization": f"Bearer {login_response.token.access_token}"}
    )
