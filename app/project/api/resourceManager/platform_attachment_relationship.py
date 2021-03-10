"""Module for the platform attachment relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.platform_attachment import PlatformAttachment
from project.api.schemas.platform_attachment_schema import PlatformAttachmentSchema
from project.api.token_checker import token_required


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
