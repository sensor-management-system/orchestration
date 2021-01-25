import os
import time
import uuid

import minio
from flask import jsonify, make_response
from project.config import BaseConfig
from urllib3.exceptions import ResponseError

config = BaseConfig()
minio_endpoint = config.MINIO_ENDPOINT
access_key = config.MINIO_ACCESS_KEY
secret_key = config.MINIO_SECRET_KEY
secure = config.MINIO_SECURE
region = config.REGION
http_client = config.HTTP_CLIENT


class MinioNotAvailableException(Exception):
    pass


class FlaskMinio:
    """This class is used to control the Minio integration to a Flask
    applications.
    """

    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".png", ".jpg", ".jpeg", ".gif"}

    def __init__(self):
        self.minio_endpoint = minio_endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.region = region
        self.http_client = http_client
        self._client = None
        self._exception_on_creating_client = None

    @property
    def client(self):
        if self._exception_on_creating_client is not None:
            raise MinioNotAvailableException(self._exception_on_creating_client)

        if self._client is None:
            try:
                self._client = minio.Minio(
                    endpoint=self.minio_endpoint,
                    access_key=self.access_key,
                    secret_key=self.secret_key,
                    secure=self.secure,
                    region=self.region,
                    http_client=self.http_client,
                )
            except ResponseError as e:
                self._exception_on_creating_client = e
                raise MinioNotAvailableException(self._exception_on_creating_client)

        return self._client

    @classmethod
    def allowed_file(cls, filename):
        return (
            "." in filename and
            os.path.splitext(filename)[-1].lower() in cls.ALLOWED_EXTENSIONS
        )

    def upload_object(self, bucket_name, uploaded_file):
        """

        :param bucket_name:
        :param uploaded_file:
        :return:
        """
        size = os.fstat(uploaded_file.fileno()).st_size
        act_year_month = time.strftime("%Y-%m")
        try:
            found = self.client.bucket_exists(bucket_name)
            if not found:
                self.client.make_bucket(bucket_name)

            if uploaded_file and self.allowed_file(uploaded_file.filename):
                filename = "{}{}".format(
                    uuid.uuid4().hex,
                    os.path.splitext(uploaded_file.filename)[-1].lower(),
                )
                ordered_filed = f"{act_year_month}/{filename}"
                self.client.put_object(bucket_name, ordered_filed, uploaded_file, size)
                data = {
                    "message": "object stored in {}".format(bucket_name),
                    "url": "http://{}/{}/{}".format(
                        self.minio_endpoint, bucket_name, ordered_filed
                    ),
                }
                response = custom_response(data, 201)

                return response
        except FileNotFoundError as e:
            return custom_response(str(e), 500)
        except Exception as e:
            return custom_response(str(e), 500)

    def remove_an_object(self, object_path):
        """

        :param object_path:
        :return:
        """
        _bucket_name, _object_name = self.extract_bucket_and_file_names_from_url(
            object_path
        )
        try:
            self.client.remove_object(_bucket_name, _object_name)
            return make_response("ok", 200)
        except ResponseError as err:
            return custom_response(str(err), 500)

    def extract_bucket_and_file_names_from_url(self, object_path):
        """
        Just in case that an other bucket name is used, we extract the name directly
        from the url.
        :param self:
        :param object_path:
        :return:
        """
        _start, _minio_endpoint, rest = object_path.partition(self.minio_endpoint + "/")
        _bucket_name, _first_slash, _object_name = rest.partition("/")
        return _bucket_name, _object_name


def custom_response(data, code):
    response = make_response(
        jsonify({"data": data, "jsonapi": {"version": "1.0"}}), code
    )
    response.headers["Content-Type"] = "application/vnd.api+json"
    return response


def error_response(code, parameter, title, detail=None):
    response = make_response(
        jsonify(
            {
                "errors": [
                    {
                        "status": code,
                        "source": {"parameter": parameter},
                        "title": title,
                        "detail": detail,
                    }
                ],
                "jsonapi": {"version": "1.0"},
            }
        )
    )
    response.headers["Content-Type"] = "application/vnd.api+json"
    return response
