from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.software_update_action_attachments import (
    PlatformSoftwareUpdateActionAttachment,
)
from project.api.schemas.software_update_action_attachment_schema import (
    PlatformSoftwareUpdateActionAttachmentSchema,
)
from project.frj_csv_export.resource import ResourceList


class PlatformSoftwareUpdateActionAttachmentList(ResourceList):
    schema = PlatformSoftwareUpdateActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }


class PlatformSoftwareUpdateActionAttachmentDetail(ResourceDetail):
    schema = PlatformSoftwareUpdateActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }


class PlatformSoftwareUpdateActionAttachmentRelationship(ResourceRelationship):
    schema = PlatformSoftwareUpdateActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }
