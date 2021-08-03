from flask import request, Blueprint

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

    if 'file' in request.files:
        file = request.files['file']
        if file and minio.allowed_file(file.filename):
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
