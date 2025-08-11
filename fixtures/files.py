import pytest
from pydantic import BaseModel

from clients.files import FilesClient, get_files_client
from fixtures.users import UserFixture
from schemas.file import UploadFileResponseSchema, UploadFileRequestSchema


class FileFixture(BaseModel):
    request: UploadFileRequestSchema
    response: UploadFileResponseSchema

    @property
    def file_id(self) -> str:
        return self.response.file.id


@pytest.fixture
def files_client(function_user: UserFixture) -> FilesClient:
    return get_files_client(function_user.authentication_user)


@pytest.fixture
def function_file(files_client: FilesClient) -> FileFixture:
    request = UploadFileRequestSchema()
    response = files_client.upload_file(request)

    return FileFixture(request=request, response=response)
