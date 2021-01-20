import os
import time
import uuid

import minio
from flask import jsonify, make_response
from urllib3.exceptions import ResponseError

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
minio_endpoint = os.getenv("MINIO_ENDPOINT", "172.16.238.10:9000")
access_key = os.getenv("MINIO_ACCESS_KEY", "minio")
secret_key = os.getenv("MINIO_SECRET_KEY", "minio123")
secure = os.getenv("MINIO_SECURE", False)
region = os.getenv("REGION", None)
http_client = os.getenv("HTTP_CLIENT", None)


class FlaskMinio(object):
    """This class is used to control the Minio integration to a Flask
    applications.
    """

    def __init__(self):
        self.minio_endpoint = minio_endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.region = region
        self.http_client = http_client
        self.client = self.client()

    def client(self):
        try:
            client = minio.Minio(
                endpoint=self.minio_endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
                region=self.region,
                http_client=self.http_client,
            )
        except ResponseError as e:
            return custom_response(str(e), 500)

        return client

    @staticmethod
    def allowed_file(filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    def upload_object(self, bucket_name, uploaded_file):
        size = os.fstat(uploaded_file.fileno()).st_size
        act_year_month = time.strftime("%Y-%m")
        try:
            found = self.client.bucket_exists(bucket_name)
            if not found:
                self.client.make_bucket(bucket_name)

            if uploaded_file and self.allowed_file(uploaded_file.filename):
                filename = "{}.{}".format(
                    uuid.uuid4().hex, uploaded_file.filename.rsplit(".", 1)[1].lower()
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
        object_name_with_bucket = object_path.partition(self.minio_endpoint + "/")[
            -1
        ].split("/")
        bucket_name = object_name_with_bucket[0]
        object_name = object_path.partition(bucket_name + "/")[-1]

        try:
            self.client.remove_object(bucket_name, object_name)
            return make_response("ok", 200)
        except ResponseError as err:
            return custom_response(str(err), 500)


def custom_response(data, code):
    response = make_response(
        jsonify({"data": data, "jsonapi": {"version": "1.0"}}), code
    )
    response.headers["Content-Type"] = "application/vnd.api+json"
    return response


def error_response(code, parameter, title, detail):
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
