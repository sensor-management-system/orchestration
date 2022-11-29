"""
Extra routes to have some verbs for sites.

As we can't add a new verb like 'archive' in the http
methods, we need to add some extra endpoints
in the style /<model_entities>/<id>/<verb> as post requests.
"""

from flask import Blueprint, g

from ..api.helpers.errors import ForbiddenError, UnauthorizedError
from ..api.models import Site
from ..api.models.base_model import db
from ..config import env
from ..restframework.rules import archive_site_permissions, restore_site_permissions
from ..restframework.shortcuts import get_object_or_404
from ..restframework.views.classbased import BaseView, class_based_view

additional_site_routes = Blueprint(
    "additional_site_routes",
    __name__,
    url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1"),
)


@additional_site_routes.route("/sites/<int:id>/archive", methods=["POST"])
@class_based_view
class ArchiveSiteView(BaseView):
    """View to archive sites with a post request."""

    permissions = archive_site_permissions
    model = Site

    def __init__(self, id):
        """Init the environment for the single request."""
        self.id = id

    def archive(self, site):
        """Archive the site."""
        if not site.archived:
            site.archived = True
            site.update_description = "archive;basic data"
            site.updated_by_id = g.user.id
            db.session.add(site)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        site = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(site):
            raise ForbiddenError("User is not allowed to archive")
        self.archive(site)
        return "", 204


@additional_site_routes.route("/sites/<int:id>/restore", methods=["POST"])
@class_based_view
class RestoreSiteView(BaseView):
    """View to restore archived sites."""

    permissions = restore_site_permissions
    model = Site

    def __init__(self, id):
        """Init the environment for the single request."""
        self.id = id

    def restore(self, site):
        """Restore the site."""
        if site.archived:
            site.archived = False
            site.update_description = "restore;basic data"
            site.updated_by_id = g.user.id
            db.session.add(site)
            db.session.commit()

    def post(self):
        """Run the post request."""
        if not self.permissions.has_permission():
            raise UnauthorizedError("Login required")
        site = get_object_or_404(self.model, self.id)
        if not self.permissions.has_object_permission(site):
            raise ForbiddenError("User is not allowed to restore")
        self.restore(site)
        return "", 204
