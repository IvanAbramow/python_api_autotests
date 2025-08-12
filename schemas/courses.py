from pydantic import BaseModel, Field, ConfigDict

from schemas.file import FileSchema
from schemas.user import UserSchema
from tools.fakers import fake


class CreatedCourseSchema(BaseModel):
    """
    Схема созданного курса, вложенная в ответ.
    """
    id: str
    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    preview_file: FileSchema = Field(alias="previewFile")
    estimated_time: str = Field(alias="estimatedTime")
    created_by_user: UserSchema = Field(alias="createdByUser")

class CreateCourseRequestSchema(BaseModel):
    """
    Описание структуры курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default="Playwright")
    max_score: int = Field(alias="maxScore", default_factory=lambda: fake.generate_random_integer(50, 100)) # Используем lambda
    min_score: int = Field(alias="minScore", default_factory=lambda: fake.generate_random_integer(10, 30)) # Используем lambda
    description: str = Field(default_factory=fake.random_text) # Убраны скобки
    preview_file_id: str = Field(alias="previewFileId")
    estimated_time: str = Field(alias="estimatedTime", default_factory=lambda: f"{fake.generate_random_integer(1, 5)} weeks") # Используем lambda
    created_by_user_id: str = Field(alias="createdByUserId")

class CreateCourseResponseSchema(BaseModel):
    course: CreatedCourseSchema

class GetCoursesRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")

class GetCourseByIdRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")

class GetCourseByIdResponseSchema(BaseModel):
    course: CreatedCourseSchema

class GetCoursesResponseSchema(BaseModel):
    courses: list[CreatedCourseSchema]

class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    description: str | None = None
    max_score: int | None = Field(alias="maxScore", default=None)
    min_score: int | None = Field(alias="minScore", default=None)
    estimated_time: str | None = Field(alias="estimatedTime", default=None)

class UpdateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления курса.
    """
    course: CreatedCourseSchema