from httpx import Client, Response, RequestError

from api_client import APIClient
from clients.private_client_builder import build_private_client
from clients.public_client_builder import build_public_client
from schemas.authentication import LoginRequestSchema
from schemas.user import CreateUserRequestSchema, UpdateUserRequestSchema, CreateUserResponseSchema


class UsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = "/api/v1/users"

    def create_request(self, payload: CreateUserRequestSchema) -> Response | RequestError:
        """
        Метод создает пользователя.

        :param payload: Словарь с email, password, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(self.url, json=payload.model_dump(by_alias=True))

    def update_request(self, payload: UpdateUserRequestSchema) -> Response | RequestError:
        """
        Метод обновления пользователя.

        :param payload: Словарь с email, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch_request(self.url, json=payload.model_dump(by_alias=True))

    def get_me_request(self) -> Response | RequestError:
        """
        Метод получения пользователя.

        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get_request(f"{self.url}/me")

    def get_by_id_request(self, user_id: str) -> Response | RequestError:
        """
        Метод получения пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.get_request(f"{self.url}/{user_id}")

    def delete_by_id_request(self, user_id: str) -> None:
        """
        Метод удаления пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete_request(f"{self.url}/{user_id}").json()

    def create_new_user(self, payload: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_request(payload)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> UsersClient:
    """
    Функция создаёт экземпляр UsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersClient.
    """
    return UsersClient(client=build_public_client())


def get_private_users_client(user: LoginRequestSchema) -> UsersClient:
    """
    Функция создаёт экземпляр UsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersClient.
    """
    return UsersClient(client=build_private_client(user))
