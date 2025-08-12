from http import HTTPStatus

import pytest

from clients.exercises import ExercisesClient
from fixtures.exercises import ExercisesFixture
from schemas.exercises import CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseByIdResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.exercises import assert_create_exercise_response, assert_get_exercise_by_id
from tools.asserts.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.exercises
class TestExercises:
    def test_create_exercise(self, exercise_client: ExercisesClient):
        request = CreateExerciseRequestSchema(title="Test")

        response = exercise_client.create_request(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_create_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise_by_id(self, exercise_client: ExercisesClient, function_exercises: ExercisesFixture):
        response = exercise_client.get_by_id_request(function_exercises.exercise_id)
        response_data = GetExerciseByIdResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_by_id(get_response=response_data, create_response=function_exercises.response)
