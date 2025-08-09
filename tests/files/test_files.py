from http import HTTPStatus

import pytest

from clients.files import FilesClient
from schemas.file import UploadFileRequestSchema, UploadFileResponseSchema
from tools.asserts.base import assert_status_code
from tools.asserts.files import assert_create_file_response
from tools.asserts.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.files
class TestFiles:
    def test_create_file(self, files_client: FilesClient):
        request = UploadFileRequestSchema(upload_file="data/image.png")
        response = files_client.upload_request(request)
        response_data = UploadFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())