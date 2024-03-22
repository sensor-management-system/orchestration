# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Routes for a proxy."""
import functools
from urllib.parse import urlparse

import requests
from flask import Blueprint, current_app, make_response, request

from ..api.helpers.errors import BadRequestError, ErrorResponse
from ..config import env

proxy_routes = Blueprint(
    "proxy", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


def build_response(resp):
    """Yield the response as chunks."""
    chunk_size = 10_000
    # See https://requests.readthedocs.io/en/latest/user/advanced/#body-content-workflow
    # and https://requests.readthedocs.io/en/latest/api/#requests.Response.iter_content
    # for the streaming approach
    for content_part in resp.iter_content(chunk_size):
        yield content_part


def handle_error_responses(f):
    """Wrap an endpoint so that we can use the json api error classes."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ErrorResponse as e:
            return e.respond()

    return wrapper


@proxy_routes.route("/proxy", methods=["GET"])
@handle_error_responses
def get_proxy():
    """Return the page with the given url."""
    url = request.args.get("url")
    if not url:
        raise BadRequestError("url paramaeter needed")
    parsed_uri = urlparse(url)
    proxy_netloc_blocklist = current_app.config["PROXY_NETLOC_BLOCKLIST"]
    if parsed_uri.netloc in proxy_netloc_blocklist:
        raise BadRequestError(f"{parsed_uri.netloc} is not supported")
    try:
        with requests.get(url) as resp:
            if not resp.ok:
                return make_response(resp.content, resp.status_code)
            resp.raise_for_status()
            content_type = resp.headers["Content-Type"]
            return current_app.response_class(
                build_response(resp), mimetype=content_type
            )
    except requests.exceptions.RequestException:
        raise BadRequestError("Request was not successful")
