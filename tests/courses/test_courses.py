from http import HTTPStatus

import pytest

from clients.courses import CoursesClient
from fixtures.courses import CoursesFixture
from schemas.courses import UpdateCourseRequestSchema, UpdateCourseResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.courses import assert_update_course_response
from tools.asserts.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.courses
class TestCourses:
    def test_update_course(self, courses_client: CoursesClient, function_course: CoursesFixture):
        request = UpdateCourseRequestSchema(description="Test")

        print(request)
        response = courses_client.update_request(function_course.course_id, request)
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
