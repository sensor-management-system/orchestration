# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

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
from ..api.permissions.rules import can_archive, can_restore, can_see
from ..config import env
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
        if not g.user:
            raise UnauthorizedError("Authentication required")
        site = get_object_or_404(self.model, self.id)
        if not can_see(site) or not can_archive(site):
            raise ForbiddenError("User is not allowed to archive")
        self.archive(site)
        return "", 204


@additional_site_routes.route("/sites/<int:id>/restore", methods=["POST"])
@class_based_view
class RestoreSiteView(BaseView):
    """View to restore archived sites."""

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
        if not g.user:
            raise UnauthorizedError("Authentication required")
        site = get_object_or_404(self.model, self.id)
        if not can_see(site) or not can_restore(site):
            raise ForbiddenError("User is not allowed to restore")
        self.restore(site)
        return "", 204
