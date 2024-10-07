# SPDX-FileCopyrightText:  2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the involved device for datastream link resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList

from ..helpers.errors import ConflictError
from ..models import (
    DatastreamLink,
    Device,
    DeviceMountAction,
    InvolvedDeviceForDatastreamLink,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.involved_device_for_datastream_link_schema import (
    InvolvedDeviceForDatastreamLinkSchema,
)
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


def ensure_create_doesnt_introduce_conflicts(model, data):
    """Throw an exception in case it doesn't make sense to create the involved device information."""
    datastream_link = db.session.query(DatastreamLink).get(data["datastream_link"])
    device_mount = datastream_link.device_mount_action
    mount_of_involved_device_in_same_configuration = (
        db.session.query(DeviceMountAction)
        .filter_by(device_id=data["device"], configuration=device_mount.configuration)
        .first()
    )
    if not mount_of_involved_device_in_same_configuration:
        raise ConflictError(
            "The involved device must be mounted in the same configuration as the datastream link"
        )


def ensure_update_doesnt_introduce_conflicts(object_):
    """Throw an exception in case it doesn't make sense to update the involved device information."""
    configuration_id = object_.datastream_link.device_mount_action.configuration_id
    device_id = object_.device.id

    mount_of_involved_device_in_same_configuration = (
        db.session.query(DeviceMountAction)
        .filter_by(device_id=device_id, configuration_id=configuration_id)
        .first()
    )
    if not mount_of_involved_device_in_same_configuration:
        raise ConflictError(
            "The involved device must be mounted in the same configuration as the datastream link"
        )


class InvolvedDeviceForDatastreamLinkList(ResourceList):
    """Resource class for lists of involved devices (GET, POST)."""

    def query(self, view_kwargs):
        """Return the (possibly) filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some checks before creating the entry."""
        ensure_create_doesnt_introduce_conflicts(self.model, data)

    schema = InvolvedDeviceForDatastreamLinkSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": InvolvedDeviceForDatastreamLink,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class InvolvedDeviceForDatastreamLinkDetail(ResourceDetail):
    """Resource class for details for involved devices (GET, PATCH, DELETE)."""

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some checks before patching the entry."""
        object_ = check_if_object_not_found(self._data_layer.model, kwargs)

        if data.get("device"):
            object_.device = db.session.query(Device).get(data["device"])
        if data.get("datastream_link"):
            object_.datastream_link = db.session.query(DatastreamLink).get(
                data["datastream_link"]
            )
        ensure_update_doesnt_introduce_conflicts(object_)

    schema = InvolvedDeviceForDatastreamLinkSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": InvolvedDeviceForDatastreamLink,
    }
    permission_classes = [DelegateToCanFunctions]
