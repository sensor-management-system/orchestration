from flask import request

from project.api import minio
from project.frj_csv_export.resource import ResourceList
from flask_rest_jsonapi.exceptions import JsonApiException, ObjectNotFound
from werkzeug.exceptions import BadRequestKeyError

from project.api.flask_minio import MinioNotAvailableException


class UploadFilesWithMinio(ResourceList):
    """
    This class allow client to ping the API.
    """

    def post(self, *args, **kwargs):
        """Create an object"""
        try:
            file = request.files["file"]
            if file.filename == "":
                raise JsonApiException({"parameter": "file"}, "No selected file")
            if file and minio.allowed_file(file.filename):
                try:
                    response = minio.upload_object(file)
                    return response, 201

                except MinioNotAvailableException as e:
                    raise JsonApiException(
                        str(e), title="Connection to MinIO server could not be done"
                    )
            else:
                raise JsonApiException(
                    {"error": "Sorry, This File Type Is Not Permitted"},
                    status=415,
                    title="Unsupported Media Type",
                )

        except BadRequestKeyError as err:
            raise JsonApiException(
                {"description": str(err.description)},
                "There is no file found in request",
                status=err.code,
                title=err.name,
            )
