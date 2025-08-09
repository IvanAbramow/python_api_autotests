import pytest
from pydantic import BaseModel

from clients.courses import CoursesClient
from clients.exercises import ExercisesClient, get_exercises_client
from fixtures.courses import CoursesFixture
from fixtures.users import UserFixture
from schemas.exercises import CreateExerciseRequestSchema, CreateExerciseResponseSchema


class ExercisesFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercise_client(function_user: UserFixture) -> ExercisesClient:
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercises(exercise_client: ExercisesClient) -> ExercisesFixture:
    request = CreateExerciseRequestSchema()
    response = exercise_client.create_new_exercise(request)

    return ExercisesFixture(request=request, response=response)
