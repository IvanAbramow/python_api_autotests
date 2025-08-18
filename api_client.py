from typing import Any

import allure
from httpx import Client, URL, Response, QueryParams, RequestError
from httpx._types import RequestData, RequestFiles


class APIClient:
    def __init__(self, client: Client):
        self.client = client

    @allure.step('GET request to url: {url}')
    def get_request(self, url: URL | str, params: QueryParams | None = None) -> Response | RequestError:
        """
        Выполняет GET-запрос.

        :param url: URL-адрес эндпоинта.
        :param params: GET-параметры запроса (например, ?key=value).
        :return: Объект Response с данными ответа.
        """
        return self.client.get(url, params=params)

    @allure.step('POST request to url: {url}')
    def post_request(
            self,
            url: URL | str,
            json: Any | None = None,
            data: RequestData | None = None,
            files: RequestFiles | None = None
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :param data: Форматированные данные формы (например, application/x-www-form-urlencoded).
        :param files: Файлы для загрузки на сервер.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url, json=json, data=data, files=files)

    @allure.step('PATCH request to url: {url}')
    def patch_request(self, url: URL | str, json: Any | None = None) -> Response | RequestError:
        """
        Выполняет PATCH-запрос (частичное обновление данных).

        :param url: URL-адрес эндпоинта.
        :param json: Данные для обновления в формате JSON.
        :return: Объект Response с данными ответа.
        """
        return self.client.patch(url, json=json)

    @allure.step('DELETE request to url: {url}')
    def delete_request(self, url: URL | str) -> Response | RequestError:
        """
        Выполняет DELETE-запрос (удаление данных).

        :param url: URL-адрес эндпоинта.
        :return: Объект Response с данными ответа.
        """
        return self.client.delete(url)
