"""Module for the device attachment detail resource."""
from flask_rest_jsonapi import ResourceDetail

from ..models.base_model import db
from ..models.device_attachment import DeviceAttachment
from ..schemas.device_attachment_schema import DeviceAttachmentSchema
from ..token_checker import token_required


class DeviceAttachmentDetail(ResourceDetail):
    """
    Resource for device attachments.

    Provides get, patch & delete methods.
    """

    schema = DeviceAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceAttachment,
    }
