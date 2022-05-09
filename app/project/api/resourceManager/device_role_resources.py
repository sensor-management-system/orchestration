"""Resource classes for the device contact roles."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..models import Device
from ..models.base_model import db
from ..models.contact_role import DeviceContactRole
from ..schemas.role import DeviceRoleSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


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
        query_ = get_query_with_permissions_for_related_objects(self.model)
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
    Detail resource for device contact roles.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device Role
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if role not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceContactRole,
    }


class DeviceRoleRelationship(ResourceRelationship):
    """
    Resource relationship for device contact roles.

    Provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Device Role and other objects.
    """

    schema = DeviceRoleSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceContactRole}
