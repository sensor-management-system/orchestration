from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from .base_resource import check_if_object_not_found
from ..models import Device
from ..models.base_model import db
from ..models.contact_role import DeviceContactRole
from ..schemas.role import DeviceRoleSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class DeviceRoleList(ResourceList):
    """
    provides get and post methods to retrieve
     a collection of Device Role or create one.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.

        Handle also additional logic to query the device
        attachments for a specific device.
        """
        query_ = self.session.query(DeviceContactRole)
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

    schema = DeviceRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceContactRole,
        "methods": {"query": query},
    }


class DeviceRoleDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device Role
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if role not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceContactRole,
    }
