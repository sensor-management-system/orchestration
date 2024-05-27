# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Routes to download uploaded files."""
import requests
from flask import Blueprint, current_app, g, redirect

from ..api.helpers.errors import ErrorResponse, ForbiddenError, UnauthorizedError
from ..api.models import (
    ConfigurationAttachment,
    DeviceAttachment,
    ExportControlAttachment,
    PlatformAttachment,
    SiteAttachment,
)
from ..api.models.base_model import db
from ..api.permissions.rules import can_see
from ..config import env

download_routes = Blueprint(
    "download", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


def build_response(url):
    """Yield the response as chunks."""
    chunk_size = 10_000
    # See https://requests.readthedocs.io/en/latest/user/advanced/#body-content-workflow
    # and https://requests.readthedocs.io/en/latest/api/#requests.Response.iter_content
    # for the streaming approach
    with requests.get(url, stream=True) as resp:
        resp.raise_for_status()
        for content_part in resp.iter_content(chunk_size):
            yield content_part


def get_content_type(url):
    """Return the content type for a minio upload."""
    resp_headers = requests.head(url)
    return resp_headers.headers["Content-Type"]


@download_routes.route("/device-attachments/<int:id>/file/<filename>", methods=["GET"])
def get_device_attachment_content(id, filename):
    """Get the file content response for the device attachment."""
    # filename will be ignored. It is just that the backend can work with
    # some urls that include them.
    device_attachment = db.session.query(DeviceAttachment).filter_by(id=id).first()
    if not device_attachment:
        return {"details": "Object not found"}, 404

    try:
        if not can_see(device_attachment):
            if not g.user:
                raise UnauthorizedError("Authentication required")
            raise ForbiddenError("Attachment not accessable")
    except ErrorResponse as e:
        return e.respond()

    if not device_attachment.is_upload:
        return redirect(device_attachment.url)

    url = device_attachment.internal_url
    mimetype = get_content_type(url)

    # See https://flask.palletsprojects.com/en/2.1.x/patterns/streaming/
    # for the streaming content
    return current_app.response_class(build_response(url), mimetype=mimetype)


@download_routes.route(
    "/platform-attachments/<int:id>/file/<filename>", methods=["GET"]
)
def get_platform_attachment_content(id, filename):
    """Get the file content response for the platform attachment."""
    platform_attachment = db.session.query(PlatformAttachment).filter_by(id=id).first()
    if not platform_attachment:
        return {"details": "Object not found"}, 404

    try:
        if not can_see(platform_attachment):
            if not g.user:
                raise UnauthorizedError("Authentication required")
            raise ForbiddenError("Attachment not accessable")
    except ErrorResponse as e:
        return e.respond()

    if not platform_attachment.is_upload:
        return redirect(platform_attachment.url)

    url = platform_attachment.internal_url
    mimetype = get_content_type(url)

    return current_app.response_class(build_response(url), mimetype=mimetype)


@download_routes.route(
    "/configuration-attachments/<int:id>/file/<filename>", methods=["GET"]
)
def get_configuration_attachment_content(id, filename):
    """Get the file content response for the configuration attachment."""
    configuration_attachment = (
        db.session.query(ConfigurationAttachment).filter_by(id=id).first()
    )
    if not configuration_attachment:
        return {"details": "Object not found"}, 404

    try:
        if not can_see(configuration_attachment):
            if not g.user:
                raise UnauthorizedError("Authentication required")
            raise ForbiddenError("Attachment not accessable")
    except ErrorResponse as e:
        return e.respond()

    if not configuration_attachment.is_upload:
        return redirect(configuration_attachment.url)

    url = configuration_attachment.internal_url
    mimetype = get_content_type(url)

    # See https://flask.palletsprojects.com/en/2.1.x/patterns/streaming/
    # for the streaming content
    return current_app.response_class(build_response(url), mimetype=mimetype)


@download_routes.route("/site-attachments/<int:id>/file/<filename>", methods=["GET"])
def get_site_attachment_content(id, filename):
    """Get the file content response for the site attachment."""
    site_attachment = db.session.query(SiteAttachment).filter_by(id=id).first()
    if not site_attachment:
        return {"details": "Object not found"}, 404

    try:
        if not can_see(site_attachment):
            if not g.user:
                raise UnauthorizedError("Authentication required")
            raise ForbiddenError("Attachment not accessable")
    except ErrorResponse as e:
        return e.respond()

    if not site_attachment.is_upload:
        return redirect(site_attachment.url)

    url = site_attachment.internal_url
    mimetype = get_content_type(url)

    # See https://flask.palletsprojects.com/en/2.1.x/patterns/streaming/
    # for the streaming content
    return current_app.response_class(build_response(url), mimetype=mimetype)


@download_routes.route(
    "/export-control-attachments/<int:id>/file/<filename>", methods=["GET"]
)
def get_export_control_attachment_content(id, filename):
    """Get the file content response for the export control attachment."""
    # filename will be ignored. It is just that the backend can work with
    # some urls that include them.
    export_control_attachment = (
        db.session.query(ExportControlAttachment).filter_by(id=id).first()
    )
    if not export_control_attachment:
        return {"details": "Object not found"}, 404

    try:
        if not can_see(export_control_attachment):
            if not g.user:
                raise UnauthorizedError("Authentication required")
            raise ForbiddenError("Attachment not accessable")
    except ErrorResponse as e:
        return e.respond()

    if not export_control_attachment.is_upload:
        return redirect(export_control_attachment.url)

    url = export_control_attachment.internal_url
    mimetype = get_content_type(url)

    # See https://flask.palletsprojects.com/en/2.1.x/patterns/streaming/
    # for the streaming content
    return current_app.response_class(build_response(url), mimetype=mimetype)
