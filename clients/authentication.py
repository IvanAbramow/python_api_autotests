from typing import TypedDict
from httpx import Client, Response

from api_client import APIClient
from clients.public_client_builder import build_public_client


class Token(TypedDict):
    """
    Описание структуры аутентификационных токенов.
    """
    tokenType: str
    accessToken: str
    refreshToken: str


class LoginPayloadDict(TypedDict):
    email: str
    password: str


class LoginResponseDict(TypedDict):
    token: Token


class RefreshPayloadDict(TypedDict):
    refreshToken: str


class AuthenticationClient(APIClient):
    """
    Клиент для работы с /api/v1/authentication
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = "/api/v1/authentication"

    def refresh_request(self, payload: RefreshPayloadDict) -> Response:
        """
        Метод обновляет токен авторизации.

        :param payload: Словарь с refreshToken.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(f"{self.url}/refresh", json=payload)

    def login_request(self, payload: LoginPayloadDict) -> Response:
        """
        Метод выполняет аутентификацию пользователя.

        :param payload: Словарь с email и password.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(f"{self.url}/login", json=payload)

    def get_token(self, payload: LoginPayloadDict) -> LoginResponseDict:
        """
        Метод выполняет аутентификацию пользователя и возвращает его токен

        :param payload: Словарь с email и password.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        response = self.login_request(payload)
        return response.json()


def get_authentication_client() -> AuthenticationClient:
    """
    Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AuthenticationClient.
    """
    return AuthenticationClient(client=build_public_client())
