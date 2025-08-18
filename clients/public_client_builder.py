from httpx import Client

from clients.event_hooks import curl_event_hook


def build_public_client() -> Client:
    """
    Функция создаёт экземпляр httpx.Client с базовыми настройками.

    :return: Готовый к использованию объект httpx.Client.
    """

    return Client(timeout=90, base_url='http://localhost:8000', event_hooks={'request': [curl_event_hook]})
