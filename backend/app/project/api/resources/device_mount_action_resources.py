# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for device mount actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..helpers.errors import ConflictError
from ..helpers.mounting_checks import DeviceMountActionValidator
from ..helpers.resource_mixin import add_updated_by_id, decode_json_request_data
from ..models import Configuration, DatastreamLink, Device, DeviceMountAction, Platform
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..resources.base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)
from ..schemas.mount_actions_schema import DeviceMountActionSchema
from ..token_checker import token_required


class DeviceMountActionList(ResourceList):
    """List resource for device mount actions (get, post)."""

    validator = DeviceMountActionValidator()

    def before_post(self, args, kwargs, data=None):
        """Run some validators before adding the entry."""
        data_with_relationships = decode_json_request_data()
        self.validator.validate_create(data_with_relationships)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")
        device_id = view_kwargs.get("device_id")
        parent_platform_id = view_kwargs.get("parent_platform_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    DeviceMountAction.configuration_id == configuration_id
                )
        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceMountAction.device_id == device_id)
        if parent_platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=parent_platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Platform: {} not found".format(parent_platform_id),
                )
            else:
                query_ = query_.filter(
                    DeviceMountAction.parent_platform_id == parent_platform_id
                )

        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;device mount action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = DeviceMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceMountAction,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceMountActionDetail(ResourceDetail):
    """Detail resource for device mount actions (get, delete, patch)."""

    validator = DeviceMountActionValidator()

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceMountAction not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data=None):
        """Do some checks (if the wanted time-interval is available or not for example)."""
        # data with relationships is almost the same as data, but it reuses the structure
        # of the request (attributes, relationships).
        data_with_relationships = decode_json_request_data()
        self.validator.validate_update(data_with_relationships, kwargs["id"])
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;device mount action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Check that we are allowed to delete."""
        self.validator.validate_delete(kwargs["id"])
        mount_action = (
            db.session.query(DeviceMountAction).filter_by(id=kwargs["id"]).one_or_none()
        )
        if mount_action is None:
            raise ObjectNotFound("Object not found!")
        if (
            db.session.query(DatastreamLink)
            .filter(DatastreamLink.device_mount_action == mount_action)
            .first()
        ):
            raise ConflictError("device mount action is linked to a datastream")
        self.tasks_after_delete = []
        configuration = mount_action.configuration
        msg = "delete;device mount action"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(configuration, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = DeviceMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceMountAction,
    }
    permission_classes = [DelegateToCanFunctions]
