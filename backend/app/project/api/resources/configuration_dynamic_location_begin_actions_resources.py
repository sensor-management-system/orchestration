# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resource classes for Configuration dynamic location begin actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..helpers.errors import ConflictError
from ..helpers.location_checks import DynamicLocationActionValidator
from ..helpers.resource_mixin import (
    add_created_by_id,
    add_updated_by_id,
    decode_json_request_data,
)
from ..models import (
    Configuration,
    ConfigurationDynamicLocationBeginAction,
    DeviceProperty,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.configuration_dynamic_location_actions_schema import (
    ConfigurationDynamicLocationBeginActionSchema,
)
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class ConfigurationDynamicLocationBeginActionList(ResourceList):
    """List resource for Configuration dynamic location begin actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        data_with_relationships = decode_json_request_data()
        DynamicLocationActionValidator().validate_create(data_with_relationships)
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the Configuration dynamic location begin actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")
        x_property_id = view_kwargs.get("x_property_id")
        y_property_id = view_kwargs.get("y_property_id")
        z_property_id = view_kwargs.get("z_property_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationDynamicLocationBeginAction.configuration_id
                    == configuration_id
                )
        if x_property_id is not None:
            try:
                self.session.query(DeviceProperty).filter_by(id=x_property_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device property: {} not found".format(x_property_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationDynamicLocationBeginAction.x_property_id
                    == x_property_id
                )
        if y_property_id is not None:
            try:
                self.session.query(DeviceProperty).filter_by(id=y_property_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device property: {} not found".format(y_property_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationDynamicLocationBeginAction.y_property_id
                    == y_property_id
                )
        if z_property_id is not None:
            try:
                self.session.query(DeviceProperty).filter_by(id=z_property_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device property: {} not found".format(z_property_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationDynamicLocationBeginAction.z_property_id
                    == z_property_id
                )
        return query_

    def after_post(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;dynamic location action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = ConfigurationDynamicLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationBeginAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ConfigurationDynamicLocationBeginActionDetail(ResourceDetail):
    """Detail resource for Configuration dynamic location begin actions (get, delete, patch)."""

    validator = DynamicLocationActionValidator()

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationDynamicLocationBeginAction ccan't be found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data=None):
        """Run some checks before patching."""
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
        msg = "update;dynamic location action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some checks before deleting."""
        location_action = (
            db.session.query(ConfigurationDynamicLocationBeginAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if location_action is None:
            raise ObjectNotFound("Object not found!")
        for x in ["x_property", "y_property", "z_property"]:
            xyz_property = getattr(location_action, x)
            if xyz_property:
                device = xyz_property.device
                if device.archived:
                    raise ConflictError("Device for property is archived")
        self.tasks_after_delete = []
        configuration = location_action.get_parent()
        msg = "delete;dynamic location action"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(configuration, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = ConfigurationDynamicLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationBeginAction,
    }
    permission_classes = [DelegateToCanFunctions]
