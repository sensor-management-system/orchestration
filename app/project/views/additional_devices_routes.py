"""
Extra routes to have some verbs for devices.

As we can't add a new verb like 'archive' in the http
methods, we need to add some extra endpoints
in the style /<model_entities>/<id>/<verb> as post requests.
"""

from flask import Blueprint, g

from ..api.helpers.errors import ForbiddenError, UnauthorizedError
from ..api.models import Device
from ..api.models.base_model import db
from ..config import env
from ..restframework.rules import (
    archive_device_permissions,
    archive_device_preconditions,
    restore_device_permissions,
)
from ..restframework.shortcuts import get_object_or_404
from ..restframework.views.classbased import BaseView, class_based_view

additional_devices_routes = Blueprint(
    "additional_devices_routes",
    __name__,
    url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1"),
)


@additional_devices_routes.route("/devices/<int:id>/archive", methods=["POST"])
@class_based_view
class ArchiveDeviceView(BaseView):
    """View to archive devices with a post request."""

    permissions = archive_device_permissions
    model = Device
    preconditions = archive_device_preconditions

    def __init__(self, id):
        """Init the environment for the single request."""
        self.id = id

    def archive(self, device):
        """Archive the device."""
        if not device.archived:
            device.archived = True
            device.update_description = "archive;basic data"
            device.updated_by_id = g.user.id
            db.session.add(device)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        device = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(device):
            raise ForbiddenError("User is not allowed to archive")
        conflict = self.preconditions.violated_by_object(device)
        if conflict:
            raise conflict
        self.archive(device)
        return "", 204


@additional_devices_routes.route("/devices/<int:id>/restore", methods=["POST"])
@class_based_view
class RestoreDeviceView(BaseView):
    """View to restore archived devices."""

    permissions = restore_device_permissions
    model = Device

    def __init__(self, id):
        """Init the envirnoment for the single request."""
        self.id = id

    def restore(self, device):
        """Restore the device."""
        if device.archived:
            device.archived = False
            device.update_description = "restore;basic data"
            device.updated_by_id = g.user.id
            db.session.add(device)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        device = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(device):
            raise ForbiddenError("User is not allowed to restore")
        self.restore(device)
        return "", 204
