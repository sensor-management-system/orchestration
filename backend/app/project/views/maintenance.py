# SPDX-FileCopyrightText: 2026
# SPDX-License-Identifier: EUPL-1.2

"""Fetch a configured maintenance document, never a client URL."""

import time

import requests
from flask import Blueprint, current_app, make_response

from ..config import env

maintenance_routes = Blueprint(
    "maintenance", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)
MAX_DOCUMENT_BYTES = 64 * 1024


@maintenance_routes.route("/maintenance-message", methods=["GET"])
def get_maintenance_message():
    """Return plain Markdown from server configuration, or no message."""
    url = current_app.config["MAINTENANCE_DOCUMENT_URL"]
    content, status = "", 204
    if url:
        try:
            with requests.get(
                url,
                timeout=(3, 5),
                allow_redirects=False,
                stream=True,
                headers={"Accept": "text/plain"},
            ) as upstream:
                if upstream.status_code != 200:
                    raise ValueError("Maintenance document request failed")
                document = bytearray()
                deadline = time.monotonic() + 10
                for chunk in upstream.iter_content(1024):
                    document.extend(chunk)
                    if (
                        len(document) > MAX_DOCUMENT_BYTES
                        or time.monotonic() > deadline
                    ):
                        raise ValueError("Maintenance download limit exceeded")
                content = document.decode("utf-8-sig")
                status = 200
        except (requests.RequestException, ValueError, UnicodeError):
            current_app.logger.warning("Unable to fetch maintenance document")
            status = 502
    response = make_response(content, status)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
