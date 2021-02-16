"""Modifications: Adopted form Custom content negotiation #171 ( miLibris /
flask-rest-jsonapi )"""
import json

from flask import make_response
from flask.wrappers import Response as FlaskResponse
from flask_rest_jsonapi.utils import JSONEncoder
from werkzeug.wrappers import Response


def parse_json(request):
    """
    Default content parser for JSON
    """
    return request.json


def render_json(response):
    """
    Default content renderer for JSON
    """
    headers = {"Content-Type": "application/vnd.api+json"}
    if isinstance(response, Response):
        response.headers.add("Content-Type", "application/vnd.api+json")
        return response

    if not isinstance(response, tuple):
        if isinstance(response, dict):
            response.update({"jsonapi": {"version": "1.0"}})
        return make_response(json.dumps(response, cls=JSONEncoder), 200, headers)

    try:
        data, status_code, headers = response
        headers.update({"Content-Type": "application/vnd.api+json"})
    except ValueError:
        pass

    try:
        data, status_code = response
    except ValueError:
        pass

    if isinstance(data, dict):
        data.update({"jsonapi": {"version": "1.0"}})

    if isinstance(data, FlaskResponse):
        data.headers.add("Content-Type", "application/vnd.api+json")
        data.status_code = status_code
        return data
    elif isinstance(data, str):
        json_reponse = data
    else:
        json_reponse = json.dumps(data, cls=JSONEncoder)

    return make_response(json_reponse, status_code, headers)


def render_csv(response):
    """
    Default content renderer for CSV
    """

    return Response(
        response.to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=export.csv"},
    )