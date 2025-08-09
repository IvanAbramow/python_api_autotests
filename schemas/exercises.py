from pydantic import BaseModel, Field, ConfigDict

from tools.fakers import fake


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(default_factory=fake.generate_uuid())
    title: str = Field(default=fake.random_text())
    course_id: str = Field(alias="courseId", default_factory=fake.generate_uuid())
    max_score: int = Field(alias="maxScore", default_factory=fake.generate_random_integer(50, 100))
    min_score: int = Field(alias="minScore", default_factory=fake.generate_random_integer(10, 30))
    order_index: int = Field(alias="orderIndex", default=fake.generate_random_integer())
    description: str = Field(default_factory=fake.random_text())
    estimated_time: str = Field(alias="estimatedTime", default=f"{fake.generate_random_integer(1, 5)} weeks")


class CreateExerciseResponseSchema(BaseModel):
    exercise: CreateExerciseRequestSchema


class GetExercisesRequestSchema(BaseModel):
    course_id: str = Field(alias="courseId")

class GetExerciseByIdRequestSchema(BaseModel):
    exercise_id: str = Field(alias="exerciseId")

class GetExerciseByIdResponseSchema(BaseModel):
    exercise: CreateExerciseRequestSchema

class GetExercisesResponseSchema(BaseModel):
    exercises: [CreateExerciseRequestSchema]
