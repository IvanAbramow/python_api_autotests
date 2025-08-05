from httpx import Client, Response

from api_client import APIClient
from clients.private_client_builder import build_private_client
from schemas.authentication import LoginRequestSchema
from schemas.courses import GetUserCoursesRequestSchema, CreateCourseRequestSchema, UpdateCourseRequestSchema, \
    CreateCourseResponseSchema


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = '/api/v1/courses'

    def get_user_courses_request(self, query: GetUserCoursesRequestSchema) -> Response:
        """
        Метод получения списка курсов.

        :param query: Словарь с userId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get_request(self.url, params=query.model_dump(by_alias=True))

    def get_by_id_request(self, course_id: str) -> Response:
        """
        Метод получения курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get_request(f"{self.url}/{course_id}")

    def create_request(self, request: CreateCourseRequestSchema) -> Response:
        """
        Метод создания курса.

        :param request: Словарь с title, maxScore, minScore, description, estimatedTime,
        previewFileId, createdByUserId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(self.url, json=request.model_dump(by_alias=True))

    def update_request(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        """
        Метод обновления курса.

        :param course_id: Идентификатор курса.
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch_request(f"{self.url}/{course_id}", json=request.model_dump(by_alias=True))

    def delete_request(self, course_id: str) -> Response:
        """
        Метод удаления курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete_request(f"{self.url}/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_request(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: LoginRequestSchema) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CoursesClient.
    """
    return CoursesClient(client=build_private_client(user))
