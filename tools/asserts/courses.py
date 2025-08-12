from schemas.courses import UpdateCourseRequestSchema, UpdateCourseResponseSchema
from tools.asserts.base import assert_equal


def assert_update_course_response(
    request: UpdateCourseRequestSchema,
    response: UpdateCourseResponseSchema):
    """
    Проверяет, что ответ на обновление курса соответствует данным из запроса.
    """

    request_data = request.model_dump(exclude_none=True)

    for field, request_value in request_data.items():
        if field in response.course.model_dump():
            response_value = getattr(response.course, field)
            assert_equal(response_value, request_value, field)
