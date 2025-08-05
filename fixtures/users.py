import pytest
from pydantic import BaseModel, EmailStr

from clients.users import UsersClient, get_public_users_client, get_private_users_client
from schemas.authentication import LoginRequestSchema
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

    @property
    def authentication_user(self) -> LoginRequestSchema:
        return LoginRequestSchema(email=self.email, password=self.password)


@pytest.fixture
def public_users_client() -> UsersClient:
    return get_public_users_client()

@pytest.fixture
def private_users_client(function_user: UserFixture) -> UsersClient:
    return get_private_users_client(function_user.authentication_user)


@pytest.fixture
def function_user(public_users_client: UsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_new_user(request)

    return UserFixture(request=request, response=response)