from httpx import Client, Response
from pathlib import Path

from api_client import APIClient
from clients.private_client_builder import build_private_client, AuthenticationUserSchema
from schemas.file import UploadFileRequestSchema, UploadFileResponseSchema


class FilesClient(APIClient):
    """
    Клиент для работы с /api/v1/files
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = '/api/v1/files'

    def upload_request(self, payload: UploadFileRequestSchema) -> Response:
        """
        Метод загрузки файла.

        :param payload: Словарь с filename, directory, upload_file.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        script_dir = Path(__file__).parent

        file_path = script_dir / 'data' / 'image.png'

        files = {
            "upload_file": open(file_path, 'rb')
        }

        return self.post_request(self.url, data=payload.model_dump(), files=files)

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

    def upload_file(self, payload: UploadFileRequestSchema) -> UploadFileResponseSchema:
        response = self.upload_request(payload)
        return UploadFileResponseSchema.model_validate_json(response.text)


def get_files_client(user: AuthenticationUserSchema) -> FilesClient:
    """
    Функция создаёт экземпляр FilesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию FilesClient.
    """
    return FilesClient(client=build_private_client(user))
