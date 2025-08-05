import uuid

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from schemas.file import FileSchema
from schemas.user import UserSchema
from tools.fakers import fake


class GetUserCoursesRequestSchema(BaseModel):
    """
    Описание структуры запроса на получение списка курсов пользователя.
    """
    user_id: str = Field(alias="userId")

class CreateCourseRequestSchema(BaseModel):
    """
    Описание структуры курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(default_factory=fake.generate_uuid())
    title: str = "Playwright"
    max_score: int = Field(alias="maxScore", default_factory=fake.generate_random_integer(50, 100))
    min_score: int = Field(alias="minScore", default_factory=fake.generate_random_integer(10, 30))
    description: str = Field(default_factory=fake.random_text())
    preview_file_id: FileSchema = Field(alias="previewFileId")
    estimated_time: str = Field(alias="estimatedTime", default=f"{fake.generate_random_integer(1, 5)} weeks")
    created_by_user_id: str = Field(alias="createdByUserId")

class CreateCourseResponseSchema(BaseModel):
    course: CreateCourseRequestSchema


class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    description: str | None
    estimated_time: str | None = Field(alias="estimatedTime")
