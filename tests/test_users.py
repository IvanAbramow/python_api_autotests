from http import HTTPStatus

import pytest

from clients.users import UsersClient
from schemas.user import CreateUserRequestSchema, CreateUserResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.schema import validate_json_schema
from tools.asserts.users import assert_create_user_data

@pytest.mark.users
@pytest.mark.regression
def test_create_user(public_users_client: UsersClient):
    request = CreateUserRequestSchema()
    create_response = public_users_client.create_request(request)

    create_response_data = CreateUserResponseSchema.model_validate_json(create_response.text)

    assert_status_code(actual=create_response.status_code, expected=HTTPStatus.OK)
    assert_create_user_data(request=request, response=create_response_data)

    validate_json_schema(create_response.json(), create_response_data.model_json_schema())




