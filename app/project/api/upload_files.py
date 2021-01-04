import os
import time
import uuid

from flask import Blueprint, jsonify, make_response, request
from minio import Minio
from urllib3.exceptions import ResponseError

from project.urls import base_url

upload_blueprint = Blueprint("upload", __name__)
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
        if file and allowed_file(file.filename):
            uploaded_file = request.files["file"]
            return upload_object(uploaded_file)
        else:

            response = error_response(
                404,
                "file",
                "Format not allowed",
                "allowed extensions are :{}".format(ALLOWED_EXTENSIONS),
            )
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


def upload_object(uploaded_file):
    bucket_name = os.getenv("MINIO_BUCKET_NAME", "smsdownloadbucket")
    size = os.fstat(uploaded_file.fileno()).st_size
    endpoint = os.getenv("MINIO_ENDPOINT", "172.16.238.10:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY", "minio")
    secret_key = os.getenv("MINIO_SECRET_KEY", "minio123")
    secure = os.getenv("MINIO_SECURE", False)
    ym = time.strftime("%Y-%m")
    try:
        minio_client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        found = minio_client.bucket_exists(bucket_name)
        if not found:
            minio_client.make_bucket(bucket_name)

        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = "{}.{}".format(
                uuid.uuid4().hex, uploaded_file.filename.rsplit(".", 1)[1].lower()
            )
            fn = f"{ym}/{filename}"
            minio_client.put_object(bucket_name, fn, uploaded_file, size)
            data = {
                "message": f"object stored in {bucket_name}",
                "url": f"http://{endpoint}/{bucket_name}/{fn}",
            }
            response = custom_response(data, 201)

            return response
    except ResponseError as e:
        return error_response(500, "MinIO server", "please contact your admin", str(e))
    except FileNotFoundError as e:
        return error_response(500, "MinIO server", "please contact your admin", str(e))
    except Exception as e:
        return error_response(500, "MinIO server", "please contact your admin", str(e))


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
