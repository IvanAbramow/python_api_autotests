from typing import TypedDict

from httpx import Client, Response

from api_client import APIClient
from clients.files import File
from clients.private_client_builder import AuthUserDict, build_private_client
from clients.users import User


class Course(TypedDict):
    """
    Описание структуры курса.
    """
    id: str
    title: str
    maxScore: int
    minScore: int
    description: str
    previewFile: File
    estimatedTime: str
    createdByUser: User

class GetUserCoursesDict(TypedDict):
    """
    Описание структуры запроса на получение списка курсов пользователя.
    """
    userId: str


class CreateCourseDict(TypedDict):
    """
    Описание структуры запроса на создание курса.
    """
    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    previewFileId: str
    createdByUserId: str

class CreateCourseResponseDict(TypedDict):
    """
    Описание структуры ответа создания курса.
    """
    course: Course

class UpdateCourseDict(TypedDict):
    """
    Описание структуры запроса на обновление курса.
    """
    title: str | None
    maxScore: int | None
    minScore: int | None
    description: str | None
    estimatedTime: str | None


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = '/api/v1/courses'

    def get_user_courses_request(self, query: GetUserCoursesDict) -> Response:
        """
        Метод получения списка курсов.

        :param query: Словарь с userId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get_request(self.url, params=query)

    def get_by_id_request(self, course_id: str) -> Response:
        """
        Метод получения курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get_request(f"{self.url}/{course_id}")

    def create_request(self, request: CreateCourseDict) -> Response:
        """
        Метод создания курса.

        :param request: Словарь с title, maxScore, minScore, description, estimatedTime,
        previewFileId, createdByUserId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(self.url, json=request)

    def update_request(self, course_id: str, request: UpdateCourseDict) -> Response:
        """
        Метод обновления курса.

        :param course_id: Идентификатор курса.
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch_request(f"{self.url}/{course_id}", json=request)

    def delete_request(self, course_id: str) -> Response:
        """
        Метод удаления курса.

        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete_request(f"{self.url}/{course_id}")

    def create_course(self, request: CreateCourseDict) -> CreateCourseResponseDict:
        response = self.create_request(request)
        return response.json()

def get_courses_client(user: AuthUserDict) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CoursesClient.
    """
    return CoursesClient(client=build_private_client(user))
