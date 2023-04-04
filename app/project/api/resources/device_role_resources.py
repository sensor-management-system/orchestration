"""Resource classes for the device contact roles."""

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..models import Device
from ..models.base_model import db
from ..models.contact_role import DeviceContactRole
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.role import DeviceRoleSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class DeviceRoleList(ResourceList):
    """
    List resource for device contact roles.

    Provides get and post methods to retrieve
    a collection of Device Role or create one.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.

        Handle also additional logic to query the device
        attachments for a specific device.
        """
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Device: {} not found".format(device_id)
                )
            query_ = query_.filter(DeviceContactRole.device_id == device_id)
        return query_

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;contact"
        query_device_and_set_update_description_text(msg, result_id)

        return result

    schema = DeviceRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceContactRole,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceRoleDetail(ResourceDetail):
    """
    Detail resource for device contact roles.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device Role
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if role not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;contact"
        query_device_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the device update description."""
        contact_role = (
            db.session.query(DeviceContactRole).filter_by(id=kwargs["id"]).one_or_none()
        )
        if contact_role is None:
            raise ObjectNotFound("Object not found!")
        device = contact_role.get_parent()
        msg = "delete;contact"
        set_update_description_text_and_update_by_user(device, msg)

    schema = DeviceRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceContactRole,
    }
    permission_classes = [DelegateToCanFunctions]
