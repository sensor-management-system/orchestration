# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Luca Johannes Nendel <luca-johannes.nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the device property list resource."""
from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...extensions.instances import pidinst
from ..helpers.errors import ConflictError
from ..helpers.resource_checks import DevicePropertyValidator
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import (
    Configuration,
    DatastreamLink,
    Device,
    DeviceMountAction,
    DeviceProperty,
    DevicePropertyCalibration,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.device_property_schema import DevicePropertySchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class DevicePropertyList(ResourceList):
    """
    List resource for device properties.

    Provides get and post methods to retrieve
    a collection of device properties or create one.
    """

    def query(self, view_kwargs):
        """
        Query all the entries from the database.

        Also handle cases to search for all the device
        properties of a specific device.
        """
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceProperty.device_id == device_id)
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Set some fields before we save the new entry."""
        add_created_by_id(data)

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;measured quantity"
        # The external device metadata are updated here.
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        # However, there is also the need to update configurations, as
        # they refer to the measured variables too.
        for configuration in (
            db.session.query(Configuration)
            .join(DeviceMountAction)
            .filter(DeviceMountAction.device_id == result_id)
        ):
            if pidinst.has_external_metadata(configuration):
                pidinst.update_external_metadata(configuration)

        return result

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
        "methods": {"query": query, "before_create_object": before_create_object},
    }
    permission_classes = [DelegateToCanFunctions]


class DevicePropertyDetail(ResourceDetail):
    """
    Detail resource class for device properties.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a device property.
    """

    validator = DevicePropertyValidator()

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceProperty not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add update info to the object."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;measured quantity"
        # The external device metadata are updated here.
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        # However, there is also the need to update configurations, as
        # they refer to the measured variables too.
        for configuration in (
            db.session.query(Configuration)
            .join(DeviceMountAction)
            .filter(DeviceMountAction.device_id == result_id)
        ):
            if pidinst.has_external_metadata(configuration):
                pidinst.update_external_metadata(configuration)
        return result

    def before_delete(self, args, kwargs):
        """Run some validations before deleting the device mount."""
        self.validator.validate_property_dynamic_location_action_deletion(kwargs["id"])
        device_property = (
            db.session.query(DeviceProperty).filter_by(id=kwargs["id"]).one_or_none()
        )
        if device_property is None:
            raise ObjectNotFound("Object not found!")
        if (
            db.session.query(DevicePropertyCalibration)
            .filter(DevicePropertyCalibration.device_property == device_property)
            .first()
        ):
            raise ConflictError("Calibration associated with device property")
        if (
            db.session.query(DatastreamLink)
            .filter(DatastreamLink.device_property == device_property)
            .first()
        ):
            raise ConflictError("Datastream associated with device property")
        self.tasks_after_delete = []
        device = device_property.get_parent()
        msg = "delete;measured quantity"

        configurations_with_external_metadata = []
        for configuration in (
            db.session.query(Configuration)
            .join(DeviceMountAction)
            .filter(DeviceMountAction.device_id == device.id)
        ):
            if pidinst.has_external_metadata(configuration):
                configurations_with_external_metadata.append(configuration)

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(device, msg)
            for configuration in configurations_with_external_metadata:
                pidinst.update_external_metadata(configuration)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
    }
    permission_classes = [DelegateToCanFunctions]
