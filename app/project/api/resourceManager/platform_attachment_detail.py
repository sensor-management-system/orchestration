"""Module for the platform attachment detail resource."""
from flask_rest_jsonapi import ResourceDetail

from project.api.models.base_model import db
from project.api.models.platform_attachment import PlatformAttachment
from project.api.schemas.platform_attachment_schema import PlatformAttachmentSchema
from project.api.token_checker import token_required


class PlatformAttachmentDetail(ResourceDetail):
    """
    Resource for platform attachments.

    Provides get, patch & delete methods.
    """

    schema = PlatformAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformAttachment,
    }
