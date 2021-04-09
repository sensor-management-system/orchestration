"""Module for the platform attachment detail resource."""
from flask_rest_jsonapi import ResourceDetail

from ..models.base_model import db
from ..models.platform_attachment import PlatformAttachment
from ..schemas.platform_attachment_schema import PlatformAttachmentSchema
from ..token_checker import token_required


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
