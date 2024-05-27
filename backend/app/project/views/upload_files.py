# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Routes for uploading files."""
from functools import wraps

from flask import Blueprint, current_app, g, request

from ..api import minio
from ..api.flask_minio import MinioNotAvailableException
from ..api.helpers.errors import (
    BadRequestError,
    ErrorResponse,
    ServiceIsUnreachableError,
    UnauthorizedError,
    UnsupportedMediaTypeError,
)
from ..config import env

upload_routes = Blueprint(
    "upload",
    __name__,
    url_prefix=env("URL_PREFIX", env("URL_PREFIX", "/rdm/svm-api/v1")),
)


def handle_error_response(f):
    """
    Wrap a view function so it that can transform ErrorResponses into flask responses.

    All decorated view functions doesn't need to take care anymore about
    the ErrorResponses, as they are transformed to response objects with
    their related error status code.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ErrorResponse as e:
            return e.respond()

    return wrapper


@upload_routes.route("/upload", methods=["POST"])
@handle_error_response
def upload():
    """Upload files."""
    if not g.user:
        raise UnauthorizedError("Authentication required")
    content_types = current_app.config["ALLOWED_MIME_TYPES"]
    if "file" in request.files:
        file = request.files["file"]
        content_type = file.content_type
        content_type_to_check = content_type
        if content_type:
            # It can be that we have content types like
            # text/csv; charset=utf-8
            # that we still want to allow, even that those are not
            # exactly in our allowed list.
            content_type_to_check = content_type.split(";", 1)[0]
        if file and content_type_to_check in content_types:
            try:
                response = minio.upload_object(file)
                return response, 201

            except MinioNotAvailableException as e:
                raise ServiceIsUnreachableError(str(e))
        else:
            raise UnsupportedMediaTypeError(
                "{} is not permitted".format(file.content_type)
            )
    else:
        raise BadRequestError("No file in request body found")
