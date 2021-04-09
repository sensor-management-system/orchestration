from flask import request, Blueprint, jsonify, make_response
from flask_rest_jsonapi.exceptions import JsonApiException
from project.api import minio
from project.api.flask_minio import MinioNotAvailableException
from project.api.token_checker import token_required

from werkzeug.exceptions import abort

upload_routes = Blueprint('upload', __name__, url_prefix="/v1")


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
                raise JsonApiException(
                    str(e), title="Connection to MinIO server could not be done"
                )
        else:
            raise JsonApiException(
                {"error": "Sorry, This File Type Is Not Permitted"},
                status=415,
                title="Unsupported Media Type",
            )
    else:
        abort(make_response(jsonify(error="Bad Request"), 400))
