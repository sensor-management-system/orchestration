"""
Extra routes to have some verbs for platforms.

As we can't add a new verb like 'archive' in the http
methods, we need to add some extra endpoints
in the style /<model_entities>/<id>/<verb> as post requests.
"""

from flask import Blueprint, g

from ..api.helpers.errors import ForbiddenError, UnauthorizedError
from ..api.models import Platform
from ..api.models.base_model import db
from ..config import env
from ..restframework.rules import (
    archive_platform_permissions,
    archive_platform_preconditions,
    restore_platform_permissions,
)
from ..restframework.shortcuts import get_object_or_404
from ..restframework.views.classbased import BaseView, class_based_view

additional_platforms_routes = Blueprint(
    "additional_platforms_routes",
    __name__,
    url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1"),
)


@additional_platforms_routes.route("/platforms/<int:id>/archive", methods=["POST"])
@class_based_view
class ArchivePlatformView(BaseView):
    """View to archive platforms with a post request."""

    permissions = archive_platform_permissions
    model = Platform
    preconditions = archive_platform_preconditions

    def __init__(self, id):
        """Init the environment for the single request."""
        self.id = id

    def archive(self, platform):
        """Archive the platform."""
        if not platform.archived:
            platform.archived = True
            platform.update_description = "archive;basic data"
            platform.updated_by_id = g.user.id
            db.session.add(platform)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        platform = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(platform):
            raise ForbiddenError("User is not allowed to archive")
        conflict = self.preconditions.violated_by_object(platform)
        if conflict:
            raise conflict
        self.archive(platform)
        return "", 204


@additional_platforms_routes.route("/platforms/<int:id>/restore", methods=["POST"])
@class_based_view
class RestorePlatformView(BaseView):
    """View to restore archived platforms."""

    permissions = restore_platform_permissions
    model = Platform

    def __init__(self, id):
        """Init the envirnoment for the single request."""
        self.id = id

    def restore(self, platform):
        """Restore the platform."""
        if platform.archived:
            platform.archived = False
            platform.update_description = "restore;basic data"
            platform.updated_by_id = g.user.id
            db.session.add(platform)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        platform = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(platform):
            raise ForbiddenError("User is not allowed to restore")
        self.restore(platform)
        return "", 204
