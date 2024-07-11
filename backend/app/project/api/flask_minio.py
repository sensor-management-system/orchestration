# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Minio related classes to handle uploads."""

import hashlib
import mimetypes
import os
import pathlib
import random
import time

import minio
from flask import _app_ctx_stack, current_app, g, make_response
from minio.error import S3Error
from urllib3.exceptions import MaxRetryError, ResponseError

from .helpers.errors import ConflictError, NotFoundError, ServiceIsUnreachableError


class MinioNotAvailableException(Exception):
    """Exception to indicate that minio is not available to work with."""

    pass


def search_a_list_of_dictionaries(lod, default, **kw):
    """Filter a list of dictionaries with the given keys & values."""
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
    """Return a filename for the uploaded file."""
    # By using the sha1, we get the same file path if we re-upload
    # the same file with the same name.
    # => That way we can save storage.
    sha1 = hashlib.sha1(uploaded_file.read()).hexdigest()
    uploaded_file.seek(0, 0)
    filename_picked_by_user = pathlib.Path(uploaded_file.filename).name
    return f"{sha1}/{filename_picked_by_user}"


class FlaskMinio:
    """
    The core Minio client object.

    This class is a class based Flask extensions used to control
    the Minio integration to a Flask applications.

    see https://flask.palletsprojects.com/en/1.1.x/extensiondev/
    """

    def __init__(self, app=None):
        """Init the object."""
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
        """Open the connection to the storage server."""
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
        """Handle the teardown when the ap stops."""
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "minio"):
            ctx.minio = None

    @property
    def connection(self):
        """
        Return the connection.

        A property that on first access opens the client
        connection and stores it on the context.
        :return:
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "minio"):
                ctx.minio = self.connect()
            return ctx.minio

    def download_endpoint(self, internal):
        """
        Return the download endpoint.

        Allows to get either the internal one (can contain a docker
        container name if it is inside a docker compose with the backend)
        or the public one.
        Using the internal one makes sure that the backend container can
        access the file ifself, while for a public one it is not granted
        (if the minio is inside the same docker compose as the backend
        ifself).

        If the minio server has its own setup then it shouldn't matter
        which one will be used.
        """
        if internal:
            protocol = "http"
            if current_app.config["MINIO_SECURE"]:
                protocol = "https"
            return f"{protocol}://{current_app.config['MINIO_ENDPOINT']}"
        return current_app.config["DOWNLOAD_ENDPOINT"]

    def upload_object(self, uploaded_file):
        """
        Upload a file as an object to the Minio Storage.

        :param uploaded_file: a file to upload.
        :return: jons:api response with a permanent url to reach that object.
        """
        size = os.fstat(uploaded_file.fileno()).st_size

        minio_bucket_name = current_app.config["MINIO_BUCKET_NAME"]
        # When we use the internal link, we can query the file in the backend
        # itself - even if the minio runs in a docker container.
        # This way we can make the download more secure by replacing the
        # url with something like /device-attachments/<id>/file and
        # are sure that the other users can't access the file itself.
        download_endpoint = self.download_endpoint(internal=True)
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
                    metadata={"uploaded-by-id": g.user.id},
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
            raise ConflictError(str(s3err))
        except MaxRetryError as e:
            self._exception_on_creating_client = e
            raise MinioNotAvailableException(self._exception_on_creating_client)

    def remove_an_object(self, object_path):
        """
        Remove an object form the Minio Storage by file path.

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

    def extract_bucket_and_file_names_from_url(self, object_path):
        """
        Extract the names for bucket & file from the url.

        Just in case that another bucket name is used, we extract the
        name directly from the url.
        :param self:
        :param object_path:
        :return:
        """
        minio_endpoint = self.download_endpoint(internal=True)
        _start, _minio_endpoint, rest = object_path.partition(minio_endpoint + "/")
        _bucket_name, _first_slash, _object_name = rest.partition("/")
        return _bucket_name, _object_name
