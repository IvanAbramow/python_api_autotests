from pydantic import BaseModel, HttpUrl


class FileSchema(BaseModel):
    id: str
    url: HttpUrl
    filename: str
    directory: str