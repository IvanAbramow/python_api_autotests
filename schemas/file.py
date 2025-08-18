from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class FileSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    url: HttpUrl
    filename: str
    directory: str

class UploadFileRequestSchema(BaseModel):
    """
    Описание структуры запроса на загрузку файла.
    """
    model_config = ConfigDict(populate_by_name=True)

    filename: str = Field(default="image.png")
    directory: str = Field(default="image.png")
    upload_file: str = Field(default="./data/files/image.png")

class UploadFileResponseSchema(BaseModel):
    """
    Описание структуры ответа загрузки файла.
    """
    file: FileSchema

class GetFileResponseSchema(BaseModel):
    """
    Описание структуры ответа получения файла.
    """
    file: FileSchema