# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for platform software update actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.platform import Platform
from ..models.software_update_actions import PlatformSoftwareUpdateAction
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..resources.base_resource import (
    check_if_object_not_found,
    query_platform_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)
from ..schemas.software_update_action_schema import PlatformSoftwareUpdateActionSchema
from .mixins.mqtt_notification import MqttNotificationMixin


class PlatformSoftwareUpdateActionList(MqttNotificationMixin, ResourceList):
    """List resource for platform software update actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific platforms, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
        platform_id = view_kwargs.get("platform_id")
        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(
                    PlatformSoftwareUpdateAction.platform_id == platform_id
                )
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["platform"]["data"]["id"]
        msg = "create;software update action"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = PlatformSoftwareUpdateActionSchema
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformSoftwareUpdateActionDetail(MqttNotificationMixin, ResourceDetail):
    """Detail relationship for platform software update actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformSoftwareUpdateAction not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add updated by user id to the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;software update action"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the platforms update description."""
        action = (
            db.session.query(PlatformSoftwareUpdateAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if action is None:
            raise ObjectNotFound("Object not found!")
        self.tasks_after_delete = []
        platform = action.get_parent()
        msg = "delete;software update action"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(platform, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = PlatformSoftwareUpdateActionSchema
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateAction,
    }
    permission_classes = [DelegateToCanFunctions]
