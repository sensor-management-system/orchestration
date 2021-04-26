"""Module for the device attachment relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from ..models.base_model import db
from ..models.device_attachment import DeviceAttachment
from ..schemas.device_attachment_schema import DeviceAttachmentSchema
from ..token_checker import token_required


class DeviceAttachmentRelationship(ResourceRelationship):
    """
    Relationship resource for device attachments.

    Provides get, post, patch & delete methods to
    retrieve, create, update or remove
    relationships between device attachments and other
    objects.
    """

    schema = DeviceAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceAttachment,
    }
