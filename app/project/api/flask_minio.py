import mimetypes
import os
import random
import time

import minio
from flask import _app_ctx_stack, current_app, make_response
from minio.error import S3Error
from urllib3.exceptions import MaxRetryError, ResponseError

from .helpers.errors import ConflictError, NotFoundError, ServiceIsUnreachableError


class MinioNotAvailableException(Exception):
    pass


def search_a_list_of_dictionaries(lod, default, **kw):
    result = list(
        filter(lambda item: (item[key] == value for (key, value) in kw.items()), lod)
    )
    if len(result) != 0:
        return result[0]
    else:
        return default


def set_file_extension(filename, content_type):
    """
    If the file extension is not set then use the content-type to guess it.

    :param filename: the uploaded name.
    :param content_type: content type from uploaded file.
    :return: string
    """
    if filename[-1] == "":
        file_extension = mimetypes.guess_extension(content_type)
    else:
        file_extension = filename[-1].lower()

    return file_extension


def set_a_filename(uploaded_file):
    act_year_month = time.strftime("%Y-%m")
    filename_picked_by_user = os.path.splitext(uploaded_file.filename)
    file_extension = set_file_extension(
        filename_picked_by_user, uploaded_file.content_type
    )
    numbers = random.randint(0, 0x10000)
    filename = "{}{}".format(
        filename_picked_by_user[0].lower() + "_" + str(numbers),
        file_extension,
    )
    ordered_filed = f"{act_year_month}/{filename}"
    return ordered_filed


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
        self._exception_on_creating_client = None
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

    def upload_object(self, uploaded_file):
        """
        Uploads a file as an object to the Minio Storage.
        :param uploaded_file: a file to upload.
        :return: jons:api response with a permanent url to reach that object.
        """
        size = os.fstat(uploaded_file.fileno()).st_size

        minio_bucket_name = current_app.config["MINIO_BUCKET_NAME"]
        download_endpoint = current_app.config["DOWNLOAD_ENDPOINT"]
        try:
            found = self.connection.bucket_exists(minio_bucket_name)
            if not found:
                # self.connection.make_bucket(minio_bucket_name)
                # self.set_bucket_policy(minio_bucket_name)
                raise NotFoundError(
                    "A Bucket with the name: {} is not Found.".format(minio_bucket_name)
                )

            if uploaded_file:
                ordered_filed = set_a_filename(uploaded_file)
                content_type = uploaded_file.content_type
                self.connection.put_object(
                    minio_bucket_name,
                    ordered_filed,
                    uploaded_file,
                    size,
                    content_type=content_type,
                    metadata={"uploaded-by-id": request.user.id},
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
            raise ConflictError(s3err.message)
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
                raise ServiceIsUnreachableError(err)

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
