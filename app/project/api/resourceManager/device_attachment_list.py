"""Module for the device attachment list resource."""
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..models.base_model import db
from ..models.device import Device
from ..models.device_attachment import DeviceAttachment
from ..schemas.device_attachment_schema import DeviceAttachmentSchema
from ..token_checker import token_required


class DeviceAttachmentList(ResourceList):
    """
    List resource for device attachments.

    Provides get and most methods to retrieve a
    collection of device attachments or to create new ones.
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
                    {"parameter": "id",}, "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceAttachment.device_id == device_id)
        return query_

    schema = DeviceAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceAttachment,
        "methods": {"query": query},
    }
