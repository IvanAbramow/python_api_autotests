import pytest
from pydantic import BaseModel

from clients.courses import CoursesClient, get_courses_client
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from schemas.courses import CreateCourseRequestSchema, CreateCourseResponseSchema


class CoursesFixture(BaseModel):
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema


@pytest.fixture
def courses_client(function_user: UserFixture) -> CoursesClient:
    return get_courses_client(function_user.authentication_user)


@pytest.fixture
def function_course(
        courses_client: CoursesClient,
        function_user: UserFixture,
        function_file: FileFixture
) -> CoursesFixture:
    request = CreateCourseRequestSchema(
        preview_file_id=function_file.response.file.id,
        created_by_user_id=function_user.response.user.id
    )
    response = courses_client.create_course(request)

    return CoursesFixture(request=request, response=response)
