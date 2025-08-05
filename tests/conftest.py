import pytest
from pydantic import BaseModel, EmailStr

from clients.authentication import AuthenticationClient, get_authentication_client
from clients.users import UsersClient, get_public_users_client
from schemas.user import CreateUserRequestSchema, CreateUserResponseSchema

class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> str:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()


@pytest.fixture
def public_users_client() -> UsersClient:
    return get_public_users_client()


@pytest.fixture
def function_user(public_users_client: UsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_new_user(request)

    return UserFixture(request=request, response=response)
