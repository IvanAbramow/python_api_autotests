from http import HTTPStatus

import pytest

from clients.authentication import AuthenticationClient
from fixtures.users import UserFixture
from schemas.authentication import LoginRequestSchema, LoginResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.schema import validate_json_schema


@pytest.mark.authentication
@pytest.mark.regression
def test_login(function_user: UserFixture, authentication_client: AuthenticationClient):
    request = LoginRequestSchema(
        email=function_user.email,
        password=function_user.password
    )
    response = authentication_client.login_request(request)
    response_data = LoginResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)

    validate_json_schema(response.json(), response_data.model_json_schema())