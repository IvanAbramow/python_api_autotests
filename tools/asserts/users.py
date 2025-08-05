from schemas.user import CreateUserRequestSchema, CreateUserResponseSchema
from tools.asserts.base import assert_equal


def assert_create_user_data(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")