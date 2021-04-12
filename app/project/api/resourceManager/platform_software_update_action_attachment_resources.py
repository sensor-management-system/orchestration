from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import delete_attachments_in_minio_by_related_object_id
from ..models import PlatformAttachment
from ..models.base_model import db
from ..models.software_update_action_attachments import (
    PlatformSoftwareUpdateActionAttachment,
)
from ..schemas.software_update_action_attachment_schema import (
    PlatformSoftwareUpdateActionAttachmentSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class PlatformSoftwareUpdateActionAttachmentList(ResourceList):
    def before_delete(self, args, kwargs):
        """Hook to delete attachment from storage server before delete method"""
        delete_attachments_in_minio_by_related_object_id(PlatformSoftwareUpdateActionAttachment,
                                                         PlatformAttachment, kwargs["id"])

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
