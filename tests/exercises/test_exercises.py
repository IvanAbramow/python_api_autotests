from http import HTTPStatus

import pytest

from clients.exercises import ExercisesClient
from schemas.exercises import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.exercises import assert_create_exercise_response
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
