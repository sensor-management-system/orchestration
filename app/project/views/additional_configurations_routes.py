"""
Extra routes to have some verbs for configurations.

As we can't add a new verb like 'archive' in the http
methods, we need to add some extra endpoints
in the style /<model_entities>/<id>/<verb> as post requests.
"""

from flask import Blueprint, g

from ..api.helpers.errors import ForbiddenError, UnauthorizedError
from ..api.models import Configuration
from ..api.models.base_model import db
from ..config import env
from ..restframework.rules import (
    archive_configuration_permissions,
    archive_configuration_preconditions,
    restore_configuration_permissions,
)
from ..restframework.shortcuts import get_object_or_404
from ..restframework.views.classbased import BaseView, class_based_view

additional_configuration_routes = Blueprint(
    "additional_configuration_routes",
    __name__,
    url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1"),
)


@additional_configuration_routes.route(
    "/configurations/<int:id>/archive", methods=["POST"]
)
@class_based_view
class ArchiveConfigurationView(BaseView):
    """View to archive configurations with a post request."""

    permissions = archive_configuration_permissions
    model = Configuration
    preconditions = archive_configuration_preconditions

    def __init__(self, id):
        """Init the environment for the single request."""
        self.id = id

    def archive(self, configuration):
        """Archive the configuration."""
        if not configuration.archived:
            configuration.archived = True
            configuration.update_description = "archive;basic data"
            configuration.updated_by_id = g.user.id
            db.session.add(configuration)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        configuration = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(configuration):
            raise ForbiddenError("User is not allowed to archive")
        conflict = self.preconditions.violated_by_object(configuration)
        if conflict:
            raise conflict
        self.archive(configuration)
        return "", 204


@additional_configuration_routes.route(
    "/configurations/<int:id>/restore", methods=["POST"]
)
@class_based_view
class RestoreConfigurationView(BaseView):
    """View to restore archived configurations."""

    permissions = restore_configuration_permissions
    model = Configuration

    def __init__(self, id):
        """Init the envirnoment for the single request."""
        self.id = id

    def restore(self, configuration):
        """Restore the configuration."""
        if configuration.archived:
            configuration.archived = False
            configuration.update_description = "restore;basic data"
            configuration.updated_by_id = g.user.id
            db.session.add(configuration)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        configuration = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(configuration):
            raise ForbiddenError("User is not allowed to restore")
        self.restore(configuration)
        return "", 204
