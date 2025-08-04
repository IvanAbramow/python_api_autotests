from typing import TypedDict

from faker import Faker
from httpx import Client, Response

from api_client import APIClient
from clients.private_client_builder import build_private_client, AuthUserDict
from clients.public_client_builder import build_public_client


class User(TypedDict):
    """
    Описание структуры пользователя.
    """
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str


class CreateUserPayloadDict(TypedDict):
    """
    Описание структуры запроса на создание пользователя.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class CreateUserResponseDict(TypedDict):
    """
    Описание структуры ответа создания пользователя.
    """
    user: User

class GetUserResponseDict(TypedDict):
    """
    Описание структуры ответа получения пользователя.
    """
    user: User

class UpdateUserDict(TypedDict):
    """
    Описание структуры запроса на обновление пользователя.
    """

    email: str | None
    lastName: str | None
    firstName: str | None
    middleName: str | None


class UsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = "/api/v1/users"

    def create_request(self, payload: CreateUserPayloadDict) -> CreateUserResponseDict:
        """
        Метод создает пользователя.

        :param payload: Словарь с email, password, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(self.url, json=payload).json()

    def update_request(self, payload: UpdateUserDict) -> GetUserResponseDict:
        """
        Метод обновления пользователя.

        :param payload: Словарь с email, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch_request(self.url, json=payload).json()

    def get_me_request(self) -> GetUserResponseDict:
        """
        Метод получения пользователя.

        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get_request("/me").json()

    def get_by_id_request(self, user_id: str) -> GetUserResponseDict:
        """
        Метод получения пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.get_request(f"/{user_id}").json()

    def delete_by_id_request(self, user_id: str) -> None:
        """
        Метод удаления пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete_request(f"/{user_id}").json()


def get_public_users_client() -> UsersClient:
    """
    Функция создаёт экземпляр UsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersClient.
    """
    return UsersClient(client=build_public_client())


def get_private_users_client(user: AuthUserDict) -> UsersClient:
    """
    Функция создаёт экземпляр UsersClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersClient.
    """
    return UsersClient(client=build_private_client(user))
