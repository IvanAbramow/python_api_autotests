from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.files import FilesClient
from fixtures.files import FileFixture
from schemas.error import ValidationErrorResponseSchema, InternalErrorResponseSchema
from schemas.file import UploadFileRequestSchema, UploadFileResponseSchema, GetFileResponseSchema
from tools.allure.annotations import AllureEpics, AllureFeatures
from tools.allure.tags import AllureTags
from tools.asserts.base import assert_status_code
from tools.asserts.errors import assert_internal_error_response
from tools.asserts.files import assert_create_file_response, assert_file, assert_create_file_with_empty_directory, \
    assert_create_file_with_empty_filename, assert_get_file_with_incorrect_file_id_response
from tools.asserts.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.files
@allure.epic(AllureEpics.LMS)
@allure.feature(AllureFeatures.FILES)
class TestFiles:
    file_path = "./data/files/image.png"

    @allure.title('Create file')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.BLOCKER)
    def test_create_file(self, files_client: FilesClient):
        request = UploadFileRequestSchema(upload_file=self.file_path)
        response = files_client.upload_request(request)
        response_data = UploadFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Get file by id')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.BLOCKER)
    def test_get_file_by_id(self, files_client: FilesClient, function_file: FileFixture):
        response = files_client.get_by_id(function_file.file_id)
        response_data = GetFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_file(response_data.file, function_file.response.file)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Delete file by id')
    @allure.tag(AllureTags.POSITIVE)
    @allure.severity(Severity.NORMAL)
    def test_delete_file(self, files_client: FilesClient, function_file: FileFixture):
        delete_response = files_client.delete_by_id(function_file.file_id)

        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = files_client.get_by_id(function_file.file_id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_internal_error_response(get_response_data, InternalErrorResponseSchema(detail="File not found"))

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())


    @allure.title('Upload file with empty filename')
    @allure.tag(AllureTags.NEGATIVE)
    @allure.severity(Severity.MINOR)
    def test_create_file_with_empty_filename(self, files_client: FilesClient):
        request = UploadFileRequestSchema(filename="", upload_file=self.file_path)
        response = files_client.upload_request(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_filename(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Upload file with empty directory')
    @allure.tag(AllureTags.NEGATIVE)
    @allure.severity(Severity.MINOR)
    def test_create_file_with_empty_directory(self, files_client: FilesClient):
        request = UploadFileRequestSchema(directory="", upload_file=self.file_path)
        response = files_client.upload_request(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_directory(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title('Get file by incorrect file id')
    @allure.tag(AllureTags.NEGATIVE)
    @allure.severity(Severity.MINOR)
    def test_get_file_with_incorrect_id(self, files_client: FilesClient, function_file: FileFixture):
        response = files_client.get_by_id(file_id="incorrect-file-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())



