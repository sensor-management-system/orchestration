from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.software_update_action_attachments import (
    PlatformSoftwareUpdateActionAttachment,
)
from ..schemas.software_update_action_attachment_schema import (
    PlatformSoftwareUpdateActionAttachmentSchema,
)
from ..token_checker import token_required


class PlatformSoftwareUpdateActionAttachmentList(ResourceList):
    schema = PlatformSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }


class PlatformSoftwareUpdateActionAttachmentDetail(ResourceDetail):
    schema = PlatformSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }


class PlatformSoftwareUpdateActionAttachmentRelationship(ResourceRelationship):
    schema = PlatformSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }
