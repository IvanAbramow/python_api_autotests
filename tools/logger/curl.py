from httpx import Request, RequestNotRead


def create_curl(request: Request, with_formatting: bool):
    """
    Собирает cURL из HTTP-запроса httpx.

    :param request: HTTP-запрос, из которого будет сформирована команда cURL.
    :return: Строка с cURL, содержащая метод запроса, URL, заголовки и тело (если есть).
    """

    result: list[str] = [f"curl -X '{request.method}'", f"'{request.url}'"]

    for header, value in request.headers.items():
        result.append(f"-H '{header}: {value}'")

    try:
        if body := request.content:
            result.append(f"-d '{body.decode('utf-8')}'")
    except RequestNotRead:
        pass

    if with_formatting:
        return " \\\n  ".join(result)
    else:
        return "".join(result)

