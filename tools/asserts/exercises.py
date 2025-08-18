from schemas.exercises import CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseByIdResponseSchema, \
    UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from tools.asserts.base import assert_equal


def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    assert_equal(request.course_id, response.exercise.course_id, 'course_id')
    assert_equal(request.title, response.exercise.title, 'title')
    assert_equal(request.description, response.exercise.description, 'description')
    assert_equal(request.order_index, response.exercise.order_index, 'order_index')
    assert_equal(request.max_score, response.exercise.max_score, 'max_score')
    assert_equal(request.min_score, response.exercise.min_score, 'min_score')


def assert_get_exercise_by_id(get_response: GetExerciseByIdResponseSchema,
                              create_response: CreateExerciseResponseSchema):
    assert_equal(get_response.exercise.id, create_response.exercise.id, 'id')
    assert_equal(get_response.exercise.title, create_response.exercise.title, 'title')
    assert_equal(get_response.exercise.description, create_response.exercise.description, 'description')
    assert_equal(get_response.exercise.max_score, create_response.exercise.max_score, 'max_score')
    assert_equal(get_response.exercise.min_score, create_response.exercise.min_score, 'min_score')
    assert_equal(get_response.exercise.order_index, create_response.exercise.order_index, 'order_index')
    assert_equal(get_response.exercise.estimated_time, create_response.exercise.estimated_time, 'estimated_time')


def assert_update_course_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema):
    """
    Проверяет, что ответ на обновление курса соответствует данным из запроса.
    """

    request_data = request.model_dump(exclude_none=True)

    for field, request_value in request_data.items():
        if field in response.exercise.model_dump():
            response_value = getattr(response.exercise, field)
            assert_equal(response_value, request_value, field)
