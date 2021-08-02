import os
import time
import uuid

import minio
from flask import current_app, _app_ctx_stack, make_response, abort, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_rest_jsonapi.exceptions import JsonApiException
from minio.error import S3Error
from urllib3.exceptions import ResponseError, MaxRetryError


class MinioNotAvailableException(Exception):
    pass


class FlaskMinio:
    """The core Minio client object.
    This class is a class based Flask extensions used to control
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
            ctx.minio = None

    @property
    def connection(self):
        """
        A property that on first access opens the client
        connection and stores it on the context.
        :return:
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "minio"):
                ctx.minio = self.connect()
            return ctx.minio

    # def set_bucket_policy(self, bucket_name):
    #     """
    #     Set bucket policy to download only, so that we can
    #     get a permanent url.
    #
    #     :param bucket_name: a string However, only characters that are
    #     valid in URLs should be used
    #
    #         :Example:
    #             Download bucket policy
    #             {
    #               "Version": "2012-10-17",
    #               "Statement": [
    #                 {
    #                   "Effect": "Allow",
    #                   "Principal": {
    #                     "AWS": [
    #                       "*"
    #                     ]
    #                   },
    #                   "Action": [
    #                     "s3:GetBucketLocation",
    #                     "s3:ListBucket"
    #                   ],
    #                   "Resource": [
    #                     "arn:aws:s3:::sms"
    #                   ]
    #                 },
    #                 {
    #                   "Effect": "Allow",
    #                   "Principal": {
    #                     "AWS": [
    #                       "*"
    #                     ]
    #                   },
    #                   "Action": [
    #                     "s3:GetObject"
    #                   ],
    #                   "Resource": [
    #                     "arn:aws:s3:::sms/*"
    #                   ]
    #                 }
    #               ]
    #             }
    #
    #     """
    #     # download_only bucket policy.
    #     policy = {
    #         "Version": "2012-10-17",
    #         "Statement": [
    #             {
    #                 "Effect": "Allow",
    #                 "Principal": {"AWS": ["*"]},
    #                 "Action": [
    #                     "s3:GetBucketLocation",
    #                     "s3:ListBucket"
    #                 ],
    #                 "Resource": [f"arn:aws:s3:::{bucket_name}"],
    #             },
    #             {
    #                 "Effect": "Allow",
    #                 "Principal": {"AWS": ["*"]},
    #                 "Action": [
    #                     "s3:GetObject",
    #                 ],
    #                 # allow to get all object under a bucket name
    #                 "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
    #             },
    #         ],
    #     }
    #
    #     self.connection.set_bucket_policy(bucket_name, json.dumps(policy))

    def allowed_file(self, filename):
        """
        Check if a file extension is allowed, which is part of the file name.

        :param filename: a string
        :return: a Boolean
        """
        return (
                "." in filename and self.get_extension(filename) in self.allowed_extensions
        )

    def get_extension(self, filename):
        """
        Return the extension of a filename.

        So for "foo.txt" return ".txt".
        """
        return os.path.splitext(filename)[-1].lower()

    def content_type(self, filename):
        """
        Try to find a specific content type.

        Use "application/octet-stream" in case we don't find a more specific one.
        """
        extension = self.get_extension(filename)
        # For those that are currently supported, it makes sense to have a more specific
        # content type, so that those files can be rendered in the browser later.
        # For extending it, you can check out
        # https://wiki.selfhtml.org/wiki/MIME-Type/%C3%9Cbersicht
        # (german page)
        content_type_by_extension = {
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
        }
        return content_type_by_extension.get(extension, "application/octet-stream")

    def upload_object(self, uploaded_file):
        """
        Uploads a file as an object to the Minio Storage.
        :param uploaded_file: a file to upload.
        :return: jons:api response with a permanent url to reach that object.
        """
        size = os.fstat(uploaded_file.fileno()).st_size
        act_year_month = time.strftime("%Y-%m")
        minio_bucket_name = current_app.config["MINIO_BUCKET_NAME"]
        download_endpoint = current_app.config["DOWNLOAD_ENDPOINT"]
        try:
            found = self.connection.bucket_exists(minio_bucket_name)
            if not found:
                # self.connection.make_bucket(minio_bucket_name)
                # self.set_bucket_policy(minio_bucket_name)
                abort(
                    make_response(
                        jsonify(
                            error="A Bucket with the name: {} is not Found.".format(
                                minio_bucket_name
                            )
                        ),
                        400,
                    )
                )

            if uploaded_file and self.allowed_file(filename=uploaded_file.filename):
                filename = "{}{}".format(
                    uuid.uuid4().hex,
                    os.path.splitext(uploaded_file.filename)[-1].lower(),
                )
                ordered_filed = f"{act_year_month}/{filename}"
                content_type = self.content_type(filename=uploaded_file.filename)
                current_user = get_jwt_identity()
                self.connection.put_object(
                    minio_bucket_name,
                    ordered_filed,
                    uploaded_file,
                    size,
                    content_type=content_type,
                    metadata={"uploaded_by": current_user}
                )
                data = {
                    "message": "object stored in {}".format(minio_bucket_name),
                    "url": "{}/{}/{}".format(
                        download_endpoint, minio_bucket_name, ordered_filed
                    ),
                }
                response = make_response(data, 201)

                return response

        except S3Error as s3err:
            raise JsonApiException({"error": s3err.message}, title=s3err.code)
        except MaxRetryError as e:
            self._exception_on_creating_client = e
            raise MinioNotAvailableException(self._exception_on_creating_client)

    def remove_an_object(self, object_path):
        """
        Removes an object form the Minio Storage by file path.
        :param object_path: a file url like:
            "http://172.16.238.10:9000/sms3/2021-02/860904cd822146b399a6d5ea48d39787.png"
        :return:
        """

        _bucket_name, _object_name = self.extract_bucket_and_file_names_from_url(
            object_path
        )
        # check if the url is not related with s3 storage
        if _bucket_name != "" and _object_name != "":
            try:
                self.connection.remove_object(_bucket_name, _object_name)
                return make_response(f"{_object_name} has been successfully removed")
            except ResponseError as err:
                raise JsonApiException({"parameter": err})

    @staticmethod
    def extract_bucket_and_file_names_from_url(object_path):
        """
        Just in case that another bucket name is used, we extract the name directly
        from the url.
        :param self:
        :param object_path:
        :return:
        """
        minio_endpoint = current_app.config["DOWNLOAD_ENDPOINT"]
        _start, _minio_endpoint, rest = object_path.partition(minio_endpoint + "/")
        _bucket_name, _first_slash, _object_name = rest.partition("/")
        return _bucket_name, _object_name
