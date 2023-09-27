# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

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
from ..api.permissions.rules import can_archive, can_restore, can_see
from ..config import env
from ..restframework.preconditions.platforms import (
    AllMountsOfPlatformAreFinishedInThePast,
    AllUsagesAsParentPlatformInDeviceMountsFinishedInThePast,
    AllUsagesAsParentPlatformInPlatformMountsFinishedInThePast,
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

    model = Platform
    preconditions = (
        AllMountsOfPlatformAreFinishedInThePast()
        & AllUsagesAsParentPlatformInDeviceMountsFinishedInThePast()
        & AllUsagesAsParentPlatformInPlatformMountsFinishedInThePast()
    )

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
        if not g.user:
            raise UnauthorizedError("Authentication required")
        platform = get_object_or_404(self.model, self.id)
        if not can_see(platform) or not can_archive(platform):
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
        if not g.user:
            raise UnauthorizedError("Authentication required")
        platform = get_object_or_404(self.model, self.id)
        if not can_see(platform) or not can_restore(platform):
            raise ForbiddenError("User is not allowed to restore")
        self.restore(platform)
        return "", 204
