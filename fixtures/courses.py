import pytest
from pydantic import BaseModel

from clients.courses import CoursesClient, get_courses_client
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from schemas.courses import CreateCourseRequestSchema, CreateCourseResponseSchema


class CoursesFixture(BaseModel):
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema

    @property
    def course_id(self) -> str:
        return self.response.course.id


@pytest.fixture
def courses_client(function_user: UserFixture) -> CoursesClient:
    return get_courses_client(function_user.authentication_user)


@pytest.fixture
def function_course(
        courses_client: CoursesClient,
        function_user: UserFixture,
        function_file: FileFixture
) -> CoursesFixture:
    print(function_file.file_id)
    print(function_user.user_id)
    request = CreateCourseRequestSchema(preview_file_id=function_file.file_id, created_by_user_id=function_user.user_id)
    response = courses_client.create_course(request)

    return CoursesFixture(request=request, response=response)
