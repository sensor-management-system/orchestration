# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""
Extra routes to have some verbs for configurations.

As we can't add a new verb like 'archive' in the http
methods, we need to add some extra endpoints
in the style /<model_entities>/<id>/<verb> as post requests.
"""

import json

from flask import Blueprint, g

from ..api.helpers.db import save_to_db
from ..api.helpers.errors import ForbiddenError, UnauthorizedError
from ..api.models import ActivityLog, Configuration
from ..api.models.base_model import db
from ..api.permissions.rules import can_archive, can_restore, can_see
from ..api.schemas.configuration_schema import ConfigurationSchema
from ..config import env
from ..extensions.instances import mqtt
from ..restframework.preconditions.configurations import (
    AllDeviceMountsForConfigurationAreFinishedInThePast,
    AllDynamicLocationsForConfigurationAreFinishedInThePast,
    AllPlatformMountsForConfigurationAreFinishedInThePast,
    AllStaticLocationsForConfigurationAreFinishedInThePast,
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

    model = Configuration
    preconditions = (
        AllDeviceMountsForConfigurationAreFinishedInThePast()
        & AllPlatformMountsForConfigurationAreFinishedInThePast()
        & AllStaticLocationsForConfigurationAreFinishedInThePast()
        & AllDynamicLocationsForConfigurationAreFinishedInThePast()
    )

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
            new_log_entry = ActivityLog.create(
                entity=configuration,
                user=g.user,
                description=configuration.update_description,
            )
            save_to_db(new_log_entry)

            mqtt.publish(
                "sms/patch-configuration",
                json.dumps(ConfigurationSchema().dump(configuration)),
            )

    def post(self):
        """Run the post request."""
        if not g.user:
            raise UnauthorizedError("Authentication required")
        configuration = get_object_or_404(self.model, self.id)
        if not can_see(configuration) or not can_archive(configuration):
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

    model = Configuration

    def __init__(self, id):
        """Init the environment for the single request."""
        self.id = id

    def restore(self, configuration):
        """Restore the configuration."""
        if configuration.archived:
            configuration.archived = False
            configuration.update_description = "restore;basic data"
            configuration.updated_by_id = g.user.id
            db.session.add(configuration)
            db.session.commit()
            new_log_entry = ActivityLog.create(
                entity=configuration,
                user=g.user,
                description=configuration.update_description,
            )
            save_to_db(new_log_entry)
            mqtt.publish(
                "sms/patch-configuration",
                json.dumps(ConfigurationSchema().dump(configuration)),
            )

    def post(self):
        """Run the post request."""
        if not g.user:
            raise UnauthorizedError("Authentication required")
        configuration = get_object_or_404(self.model, self.id)
        if not can_see(configuration) or not can_restore(configuration):
            raise ForbiddenError("User is not allowed to restore")
        self.restore(configuration)
        return "", 204
