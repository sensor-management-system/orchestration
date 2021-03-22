"""Module for the platform attachment relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from ..models.base_model import db
from ..models.platform_attachment import PlatformAttachment
from ..schemas.platform_attachment_schema import PlatformAttachmentSchema
from ..token_checker import token_required


class PlatformAttachmentRelationship(ResourceRelationship):
    """
    Relationship resource for platform attachments.

    Provides get, post, patch & delete methods to
    retrieve, create, update or remove
    relationships between platform attachments and other
    objects.
    """

    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
    }
