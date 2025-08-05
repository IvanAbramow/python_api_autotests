from faker.proxy import Faker
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserSchema(BaseModel):
    """
    Описание структуры пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание пользователя.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: str = Field(default_factory=lambda: str(Faker.email()))
    password: str = Field(default_factory=lambda: str(Faker.password()))
    last_name: str = Field(alias="lastName", default_factory=lambda: str(Faker.last_name()))
    first_name: str = Field(alias="firstName", default_factory=lambda: str(Faker.first_name()))
    middle_name: str = Field(alias="middleName", default_factory=lambda: str(Faker.middle_name()))

class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserSchema

class UpdateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление пользователя.
    """

    model_config = ConfigDict(populate_by_name=True)

    email: str | None
    last_name: str | None = Field(alias="lastName")
    first_name: str | None = Field(alias="firstName")
    middle_name: str | None = Field(alias="middleName")

class UpdateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления пользователя.
    """
    user: UserSchema

class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа получения пользователя.
    """
    user: UserSchema