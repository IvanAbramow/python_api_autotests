from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.users import UsersClient
from fixtures.users import UserFixture
from schemas.user import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.allure.annotations import AllureEpics, AllureFeatures
from tools.allure.tags import AllureTags
from tools.asserts.base import assert_status_code
from tools.asserts.schema import validate_json_schema
from tools.asserts.users import assert_create_user_data, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@allure.epic(AllureEpics.LMS)
@allure.feature(AllureFeatures.USERS)
class TestUsers:
    @pytest.mark.parametrize("domain", ["mail.ru", "gmail.com", "example.com"],
                             ids=lambda domain: f"user with {domain} email")
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.BLOCKER)
    def test_create_user(self, domain: str, public_users_client: UsersClient):
        allure.dynamic.title(f"Create user with email: {domain}")

        request = CreateUserRequestSchema(email=fake.generate_email(domain=domain))
        create_response = public_users_client.create_request(request)

        create_response_data = CreateUserResponseSchema.model_validate_json(create_response.text)

        assert_status_code(actual=create_response.status_code, expected=HTTPStatus.OK)
        assert_create_user_data(request=request, response=create_response_data)

        validate_json_schema(create_response.json(), create_response_data.model_json_schema())

    @allure.title('Get user me')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.CRITICAL)
    def test_get_user_me(self, function_user: UserFixture, private_users_client: UsersClient):
        response = private_users_client.get_me_request()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        assert_get_user_response(get_user_response=response_data, create_user_response=function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())
