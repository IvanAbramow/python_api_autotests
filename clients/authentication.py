import allure
from httpx import Client, Response

from api_client import APIClient
from clients.public_client_builder import build_public_client
from schemas.authentication import RefreshRequestSchema, LoginRequestSchema, LoginResponseSchema


class AuthenticationClient(APIClient):
    """
    Клиент для работы с /api/v1/authentication
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = "/api/v1/authentication"

    @allure.step('Refresh authorized token')
    def refresh_request(self, payload: RefreshRequestSchema) -> Response:
        """
        Метод обновляет токен авторизации.

        :param payload: Словарь с refreshToken.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(f"{self.url}/refresh", json=payload.model_dump(by_alias=True))

    @allure.step('Login request')
    def login_request(self, payload: LoginRequestSchema) -> Response:
        """
        Метод выполняет аутентификацию пользователя.

        :param payload: Словарь с email и password.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(f"{self.url}/login", json=payload.model_dump(by_alias=True))

    @allure.step('Get authorized token')
    def get_token(self, payload: LoginRequestSchema) -> LoginResponseSchema:
        """
        Метод выполняет аутентификацию пользователя и возвращает его токен

        :param payload: Словарь с email и password.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        response = self.login_request(payload)
        return LoginResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    """
    Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AuthenticationClient.
    """
    return AuthenticationClient(client=build_public_client())
