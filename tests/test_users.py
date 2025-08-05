from http import HTTPStatus

import pytest

from clients.users import UsersClient
from schemas.user import CreateUserRequestSchema, CreateUserResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.schema import validate_json_schema
from tools.asserts.users import assert_create_user_data
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "example.com"], ids= lambda domain: f"user with {domain} email" )
def test_create_user(domain: str, public_users_client: UsersClient):
    request = CreateUserRequestSchema(email=fake.generate_email(domain=domain))
    create_response = public_users_client.create_request(request)

    create_response_data = CreateUserResponseSchema.model_validate_json(create_response.text)

    assert_status_code(actual=create_response.status_code, expected=HTTPStatus.OK)
    assert_create_user_data(request=request, response=create_response_data)

    validate_json_schema(create_response.json(), create_response_data.model_json_schema())




