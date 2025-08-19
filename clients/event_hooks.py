import allure
from httpx import Request, Response

from tools.logger.curl import create_curl
from tools.logger.logger import get_logger

logger = get_logger()

def curl_event_hook(request: Request):
    """
    Event hook для автоматического прикрепления cURL команды к Allure отчету.

    :param request: HTTP-запрос, переданный в `httpx` клиент.
    """
    allure.attach(create_curl(request, True), "cURL:", allure.attachment_type.TEXT)

def log_request_event_hook(request: Request):
    """
    Логирует информацию об отправленном HTTP-запросе.

    :param request: Объект запроса HTTPX.
    """
    logger.info(f'Request: {create_curl(request, False)}')


def log_response_event_hook(response: Response):
    """
    Логирует информацию о полученном HTTP-ответе.

    :param response: Объект ответа HTTPX.
    """
    logger.info(
        f"Response: {response.status_code} {response.reason_phrase}"
    )