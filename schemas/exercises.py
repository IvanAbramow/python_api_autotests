from pydantic import BaseModel, Field, ConfigDict

from tools.fakers import fake


class ExerciseSchema(BaseModel):
    id: str
    title: str
    description: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    estimated_time: str = Field(alias="estimatedTime")


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=lambda: fake.random_text())
    description: str = Field(default_factory=lambda: fake.random_text())
    course_id: str = Field(alias="courseId", default_factory=fake.generate_uuid)
    max_score: int = Field(alias="maxScore", default_factory=lambda: fake.generate_random_integer(50, 100))
    min_score: int = Field(alias="minScore", default_factory=lambda: fake.generate_random_integer(10, 30))
    order_index: int = Field(alias="orderIndex", default_factory=lambda: fake.generate_random_integer(10, 30))
    estimated_time: str = Field(alias="estimatedTime",
                                default_factory=lambda: f"{fake.generate_random_integer(1, 5)} weeks")


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    description: str | None = None
    max_score: int | None = Field(alias="maxScore", default=None)
    min_score: int | None = Field(alias="minScore", default=None)
    order_index: int | None = Field(alias="orderIndex", default=None)
    estimated_time: str | None = Field(alias="estimatedTime", default=None)

class UpdateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class CreateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class GetExercisesRequestSchema(BaseModel):
    course_id: str = Field(alias="courseId")


class GetExerciseByIdRequestSchema(BaseModel):
    exercise_id: str = Field(alias="exerciseId")


class GetExerciseByIdResponseSchema(BaseModel):
    exercise: ExerciseSchema


class GetExercisesResponseSchema(BaseModel):
    exercises: list[ExerciseSchema]
