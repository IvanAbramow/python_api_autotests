from typing import TypedDict

from httpx import Client, Response

from api_client import APIClient
from clients.private_client_builder import build_private_client


class File(TypedDict):
    """
    Описание структуры файла.
    """
    id: str
    url: str
    filename: str
    directory: str


class UploadFileDict(TypedDict):
    """
    Описание структуры запроса на создание файла.
    """
    filename: str
    directory: str
    upload_file: str


class UploadFileResponseDict(TypedDict):
    """
    Описание структуры ответа создания файла.
    """
    file: File


class FilesClient(APIClient):
    """
    Клиент для работы с /api/v1/files
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = '/api/v1/files'

    def upload_request(self, payload: UploadFileDict) -> Response:
        """
        Метод загрузки файла.

        :param payload: Словарь с filename, directory, upload_file.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        files = {
            "upload_file": open(payload["upload_file"], 'rb')
        }

        return self.post_request(self.url, data=payload, files=files)

    def get_by_id(self, file_id: str) -> Response:
        """
        Метод получения файла по id.

        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.get_request(f"{self.url}/{file_id}")

    def delete_by_id(self, file_id: str) -> Response:
        """
        Метод удаления файла по id.

        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.delete_request(f"{self.url}/{file_id}")

    def upload_file(self, payload: UploadFileDict) -> UploadFileResponseDict:
        return self.upload_request(payload).json()


def get_files_client(user: AuthUserDict) -> FilesClient:
    """
    Функция создаёт экземпляр FilesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию FilesClient.
    """
    return FilesClient(client=build_private_client(user))
