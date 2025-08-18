import allure
from httpx import Request

from tools.logger.curl import create_curl


def curl_event_hook(request: Request):
    """
    Event hook для автоматического прикрепления cURL команды к Allure отчету.

    :param request: HTTP-запрос, переданный в `httpx` клиент.
    """
    allure.attach(create_curl(request), "cURL:", allure.attachment_type.TEXT)