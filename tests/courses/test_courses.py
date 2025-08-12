from http import HTTPStatus

import pytest

from clients.courses import CoursesClient
from fixtures.courses import CoursesFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from schemas.courses import UpdateCourseRequestSchema, UpdateCourseResponseSchema, GetCoursesRequestSchema, \
    GetCourseByIdResponseSchema, GetCoursesResponseSchema, CreateCourseRequestSchema, CreateCourseResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.courses import assert_update_course_response, assert_get_courses_response, \
    assert_create_course_response
from tools.asserts.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.courses
class TestCourses:
    def test_create_course(self, courses_client: CoursesClient, function_file: FileFixture, function_user: UserFixture):
        request = CreateCourseRequestSchema(previewFileId=function_file.file_id, createdByUserId=function_user.user_id)

        response = courses_client.create_request(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_course(self, courses_client: CoursesClient, function_course: CoursesFixture):
        request = UpdateCourseRequestSchema(description="Test")

        response = courses_client.update_request(function_course.course_id, request)
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_courses_by_course_id(
            self,
            courses_client: CoursesClient,
            function_course: CoursesFixture
    ):
        response = courses_client.get_by_id_request(function_course.course_id)
        response_data = GetCourseByIdResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_courses_by_user_id(
            self,
            courses_client: CoursesClient,
            function_course: CoursesFixture,
            function_user: UserFixture
    ):
        request = GetCoursesRequestSchema(userId=function_user.user_id)
        response = courses_client.get_user_courses_request(request)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_courses_response(response_data, [function_course.response])
        validate_json_schema(response.json(), response_data.model_json_schema())
