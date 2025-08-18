import allure

from schemas.user import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.asserts.base import assert_equal


@allure.step("Check create user response body")
def assert_create_user_data(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

def assert_user(request: GetUserResponseSchema, response: CreateUserResponseSchema):
    assert_equal(response.user.id, request.user.id, "id")
    assert_equal(response.user.email, request.user.email, "email")
    assert_equal(response.user.last_name, request.user.last_name, "last_name")
    assert_equal(response.user.first_name, request.user.first_name, "first_name")
    assert_equal(response.user.middle_name, request.user.middle_name, "middle_name")

@allure.step("Check get user response body")
def assert_get_user_response(get_user_response: GetUserResponseSchema, create_user_response: CreateUserResponseSchema):
    assert_user(response=create_user_response, request=get_user_response)