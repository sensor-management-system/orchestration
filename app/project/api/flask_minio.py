import json
import os
import time
import uuid

from flask import current_app, _app_ctx_stack
import minio
from flask import jsonify, make_response
from urllib3.exceptions import ResponseError


class MinioNotAvailableException(Exception):
    pass


class FlaskMinio:
    """The core Minio client object.
    This class isa Class based Flask extensions used to control
    the Minio integration to a Flask applications.

    see https://flask.palletsprojects.com/en/1.1.x/extensiondev/
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
         Do setup that requires a Flask app.
         This method exists so that the FlaskMinio object can be
         instantiated without requiring an app object.

        :param app: The application to initialize
        """
        # Set some default configuration options
        app.config.setdefault("REGION", None)
        app.config.setdefault("HTTP_CLIENT", None)
        # should ONLY be turned off for local debugging
        app.config.setdefault("MINIO_SECURE", True)
        app.config.setdefault("MINIO_REGION", None)
        allowed_extensions = [".txt", ".pdf", ".png", ".jpg", ".jpeg", ".gif"]
        app.config.setdefault("ALLOWED_EXTENSIONS", allowed_extensions)
        self._exception_on_creating_client = None
        self.allowed_extensions = app.config["ALLOWED_EXTENSIONS"]
        app.teardown_appcontext(self.teardown)

    def connect(self):
        """
        This method opens a connection to the storage server.
        :return:
        """
        if self._exception_on_creating_client is not None:
            raise MinioNotAvailableException(self._exception_on_creating_client)

        try:
            return minio.Minio(
                endpoint=current_app.config["MINIO_ENDPOINT"],
                access_key=current_app.config["MINIO_ACCESS_KEY"],
                secret_key=current_app.config["MINIO_SECRET_KEY"],
                secure=current_app.config["MINIO_SECURE"],
                region=current_app.config["MINIO_REGION"],
                http_client=current_app.config["MINIO_HTTP_CLIENT"],
            )
        except ResponseError as e:
            self._exception_on_creating_client = e
            raise MinioNotAvailableException(self._exception_on_creating_client)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "minio"):
            ctx.minio._http.clear()

    @property
    def connection(self):
        """
        property that on first access opens the client
        connection and stores it on the context
        :return:
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "minio"):
                ctx.minio = self.connect()
            return ctx.minio

    def set_bucket_policy(self, bucket_name):
        """
        Set bucket policy to download only so that we can
        get a permanent url
        :param bucket_name:
        """
        # download_only bucket policy.
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": [
                        "s3:GetBucketLocation",
                        "s3:ListBucket",
                        "s3:ListBucketMultipartUploads",
                    ],
                    "Resource": [f"arn:aws:s3:::{bucket_name}"],
                },
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": [
                        "s3:GetObject",
                        # "s3:PutObject",
                        # "s3:DeleteObject",
                        # "s3:ListMultipartUploadParts",
                        # "s3:AbortMultipartUpload",
                    ],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
                },
            ],
        }

        self.connection.set_bucket_policy(bucket_name, json.dumps(policy))

    def allowed_file(self, filename):
        return ("." in filename and os.path.splitext(filename)[-1].lower() in
                set(self.allowed_extensions)
                )

    def upload_object(self, uploaded_file):
        """

        :param uploaded_file:
        :return:
        """
        size = os.fstat(uploaded_file.fileno()).st_size
        act_year_month = time.strftime("%Y-%m")
        minio_bucket_name = current_app.config["MINIO_BUCKET_NAME"]
        minio_endpoint = current_app.config["MINIO_ENDPOINT"]
        try:
            found = self.connection.bucket_exists(minio_bucket_name)
            if not found:
                self.connection.make_bucket(minio_bucket_name)
                self.set_bucket_policy(minio_bucket_name)

            if uploaded_file and self.allowed_file(filename=uploaded_file.filename):
                filename = "{}{}".format(
                    uuid.uuid4().hex,
                    os.path.splitext(uploaded_file.filename)[-1].lower(),
                )
                ordered_filed = f"{act_year_month}/{filename}"
                self.connection.put_object(
                    minio_bucket_name, ordered_filed, uploaded_file, size
                )
                data = {
                    "message": "object stored in {}".format(minio_bucket_name),
                    "url": "http://{}/{}/{}".format(
                        minio_endpoint, minio_bucket_name, ordered_filed
                    ),
                }
                response = custom_response(data, 201)

                return response
            else:
                response = error_response(
                    404,
                    "file",
                    "Format not allowed",
                    "allowed extensions are :{}".format(self.allowed_extensions),
                )
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
            self.connection.remove_object(_bucket_name, _object_name)
            return make_response("ok", 200)
        except ResponseError as err:
            return custom_response(str(err), 500)

    def extract_bucket_and_file_names_from_url(self, object_path):
        """
        Just in case that another bucket name is used, we extract the name directly
        from the url.
        :param self:
        :param object_path:
        :return:
        """
        minio_endpoint = current_app.config["MINIO_ENDPOINT"]
        _start, _minio_endpoint, rest = object_path.partition(minio_endpoint + "/")
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
