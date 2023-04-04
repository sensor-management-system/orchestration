"""Resource classes for the datastream links."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, DatastreamLink, DeviceMountAction, DeviceProperty
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.datastream_link_schema import DatastreamLinkSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_and_set_update_description_text,
)


def ensure_create_doesnt_introduce_conflicts(model, data):
    """Throw an exception in case it doesn't make sense to create the link."""
    # First we test if we are working with the very same device (mount & property)
    device_mount = db.session.query(DeviceMountAction).get(data["device_mount_action"])
    device_property = db.session.query(DeviceProperty).get(data["device_property"])
    if not device_mount.device == device_property.device:
        raise ConflictError(
            "Mount and device property doesn't belong to the same device"
        )


def ensure_update_doesnt_introduce_conflicts(object_):
    """Throw an exception in case it doesn't make sense to update the link."""
    # First we test if we are working with the very same device (mount & property)
    device_mount = object_.device_mount_action
    device_property = object_.device_property
    if not device_mount.device == device_property.device:
        raise ConflictError(
            "Mount and device property doesn't belong to the same device"
        )


class DatastreamLinkList(ResourceList):
    """List resource for datastream links (get, post)."""

    def query(self, view_kwargs):
        """Query the entries from the database."""
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")

        if configuration_id is not None:
            try:
                # This will result in the ObjectNotFound
                (self.session.query(Configuration).filter_by(id=configuration_id).one())
                # and this will filter our query_
                # However: we don't need to join as our visibility check
                # in the permission handling does that already.
                # We can just filter at the moment.
                query_ = query_.filter(Configuration.id == configuration_id)

            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Configuration: {} not found".format(configuration_id),
                )

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some checks before creating the entry."""
        ensure_create_doesnt_introduce_conflicts(self.model, data)
        add_created_by_id(data)

    def after_post(self, result):
        """Add some information in related objects."""
        device_mount_action = db.session.query(DeviceMountAction).get(
            result[0]["data"]["relationships"]["device_mount_action"]["data"]["id"]
        )
        msg = "create;datastream link"
        query_configuration_and_set_update_description_text(
            msg, device_mount_action.configuration_id
        )
        return result

    schema = DatastreamLinkSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DatastreamLink,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DatastreamLinkDetail(ResourceDetail):
    """Detail resource for datastream links (get, patch, delete)."""

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some logic (preconditions) before patching."""
        object_ = check_if_object_not_found(self._data_layer.model, kwargs)

        # We also check if after the updates.
        if data.get("device_mount_action"):
            object_.device_mount_action = db.session.query(DeviceMountAction).get(
                data["device_mount_action"]
            )
        if data.get("device_property"):
            object_.device_property = db.session.query(DeviceProperty).get(
                data["device_property"]
            )
        ensure_update_doesnt_introduce_conflicts(object_)
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after the patch & return the result."""
        device_mount_action = db.session.query(DeviceMountAction).get(
            result["data"]["relationships"]["device_mount_action"]["data"]["id"]
        )
        msg = "update;datastream link"
        query_configuration_and_set_update_description_text(
            msg, device_mount_action.configuration_id
        )

        return result

    def before_delete(self, args, kwargs):
        """Run some logic before we delete the entry."""
        object_ = check_if_object_not_found(self._data_layer.model, kwargs)
        device_mount_action = object_.device_mount_action
        msg = "delete;datastream link"
        query_configuration_and_set_update_description_text(
            msg, device_mount_action.configuration_id
        )

    schema = DatastreamLinkSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DatastreamLink,
    }
    permission_classes = [DelegateToCanFunctions]
