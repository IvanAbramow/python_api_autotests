from functools import lru_cache

from httpx import Client
from pydantic import BaseModel

from clients.authentication import get_authentication_client
from clients.event_hooks import curl_event_hook
from config import settings
from schemas.authentication import LoginRequestSchema


class AuthenticationUserSchema(BaseModel, frozen=True):
    email: str
    password: str

@lru_cache(maxsize=None)  # Кешируем возвращаемое значение
def build_private_client(user: AuthenticationUserSchema) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    :param user: Объект AuthenticationUserSchema с email и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """
    authentication_client = get_authentication_client()

    payload = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.get_token(payload)

    return Client(
        timeout=settings.http_client.timeout,
        base_url=settings.http_client.base_url,
        headers={"Authorization": f"Bearer {login_response.token.access_token}"},
        event_hooks={'request': [curl_event_hook]}
    )
