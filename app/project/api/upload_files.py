from flask import Blueprint, request
from project.api.flask_minio import FlaskMinio, error_response
from project.urls import base_url

from project.api import minio

upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route(f"{base_url}/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has a file
        if "file" not in request.files:
            response = error_response(404, "file", "No file found", None)
            return response
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            response = error_response(
                404, "file", "No file selected", "You didn't select file"
            )
            return response
        if file:
            uploaded_file = request.files["file"]
            response = minio.upload_object(uploaded_file)

            return response

    return """
    <!doctype html>
    <title>Upload a File to Minio</title>
    <h1>Upload your File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """
