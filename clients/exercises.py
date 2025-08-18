from httpx import Client, Response, RequestError

from api_client import APIClient
from clients.private_client_builder import build_private_client, AuthenticationUserSchema
from schemas.exercises import CreateExerciseRequestSchema, CreateExerciseResponseSchema, UpdateExerciseRequestSchema


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.url = "/api/v1/exercises"

    def create_request(self, payload: CreateExerciseRequestSchema) -> Response | RequestError:
        """
        Метод создает задание.

        :param payload: Словарь с email, password, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post_request(self.url, json=payload.model_dump(by_alias=True, exclude_none=True))

    def get_by_id_request(self, exercise_id: str) -> Response | RequestError:
        """
        Метод получения задания по идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.get_request(f"{self.url}/{exercise_id}")

    def delete_by_id_request(self, exercise_id: str) -> Response | RequestError:
        """
        Метод удаления задания по идентификатору.

        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.delete_request(f"{self.url}/{exercise_id}")

    def update_by_id_request(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response | RequestError:
        """
        Метод обновления задания по идентификатору.

        :param payload: UpdateExerciseRequestSchema
        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.patch_request(f"{self.url}/{exercise_id}", json=request.model_dump(by_alias=True, exclude_none=True))

    def get_all_by_course_id_request(self, course_id: str) -> Response | RequestError:
        """
        Метод получения всех заданий курса

        :param course_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        return self.get_request(f"{self.url}/{course_id}")

    def create_new_exercise(self, payload: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_request(payload)
        return CreateExerciseResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=build_private_client(user))
