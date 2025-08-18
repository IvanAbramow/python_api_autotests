from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.exercises import ExercisesClient
from fixtures.exercises import ExercisesFixture
from schemas.error import InternalErrorResponseSchema
from schemas.exercises import CreateExerciseRequestSchema, CreateExerciseResponseSchema, GetExerciseByIdResponseSchema, \
    UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesResponseSchema, GetExercisesRequestSchema
from tools.allure.annotations import AllureEpics, AllureFeatures
from tools.allure.tags import AllureTags
from tools.asserts.base import assert_status_code
from tools.asserts.errors import assert_internal_error_response
from tools.asserts.exercises import assert_create_exercise_response, assert_get_exercise_by_id, \
    assert_update_course_response
from tools.asserts.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.exercises
@allure.epic(AllureEpics.LMS)
@allure.feature(AllureFeatures.EXERCISES)
class TestExercises:
    @allure.title('Create exercise')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.BLOCKER)
    def test_create_exercise(self, exercise_client: ExercisesClient):
        request = CreateExerciseRequestSchema(title="Test")

        response = exercise_client.create_request(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_create_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Get exercise by id')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.BLOCKER)
    def test_get_exercise_by_id(self, exercise_client: ExercisesClient, function_exercises: ExercisesFixture):
        response = exercise_client.get_by_id_request(function_exercises.exercise_id)
        response_data = GetExerciseByIdResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_by_id(get_response=response_data, create_response=function_exercises.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Get exercises by course id')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.BLOCKER)
    def test_get_exercises(self, exercise_client: ExercisesClient,
                           function_exercises: ExercisesFixture):
        response = exercise_client.get_all_by_course_id_request(
            GetExercisesRequestSchema(courseId=function_exercises.response.exercise.course_id))
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert len(response_data.exercises) == 1

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Update exercise')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.CRITICAL)
    def test_update_exercise(self, exercise_client: ExercisesClient, function_exercises: ExercisesFixture):
        request = UpdateExerciseRequestSchema(description="Test")

        response = exercise_client.update_by_id_request(function_exercises.exercise_id, request)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Delete exercise')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.NORMAL)
    def test_delete_exercise(self, exercise_client: ExercisesClient, function_exercises: ExercisesFixture):
        delete_response = exercise_client.delete_by_id_request(function_exercises.exercise_id)

        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = exercise_client.get_by_id_request(function_exercises.exercise_id)
        response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_internal_error_response(response_data, InternalErrorResponseSchema(detail="Exercise not found"))

        validate_json_schema(get_response.json(), response_data.model_json_schema())
