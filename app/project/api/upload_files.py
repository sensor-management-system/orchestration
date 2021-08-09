from flask import request, Blueprint, current_app

from .flask_minio import MinioNotAvailableException
from .helpers.errors import UnsupportedMediaTypeError, BadRequestError, ServiceIsUnreachableError
from .token_checker import token_required
from ..api import minio
from ..config import env

upload_routes = Blueprint('upload', __name__,
                          url_prefix=env("URL_PREFIX", env("URL_PREFIX", "/rdm/svm-api/v1")))


@upload_routes.route('/upload', methods=['POST'])
@token_required
def upload():
    """Upload route"""
    content_types = current_app.config["ALLOWED_MIME_TYPES"]
    if 'file' in request.files:
        file = request.files['file']
        content_type = file.content_type
        if file and content_type in content_types:
            try:
                response = minio.upload_object(file)
                return response, 201

            except MinioNotAvailableException as e:
                raise ServiceIsUnreachableError(str(e))
        else:
            raise UnsupportedMediaTypeError(
                "{} is Not Permitted".format(file.content_type)
            )
    else:
        raise BadRequestError("No File in request Body was Found")
