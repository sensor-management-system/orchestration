from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import delete_attachments_in_minio_by_related_object_id
from ..models import DeviceAttachment
from ..models.base_model import db
from ..models.software_update_action_attachments import (
    DeviceSoftwareUpdateActionAttachment,
)
from ..schemas.software_update_action_attachment_schema import (
    DeviceSoftwareUpdateActionAttachmentSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class DeviceSoftwareUpdateActionAttachmentList(ResourceList):
    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}


class DeviceSoftwareUpdateActionAttachmentDetail(ResourceDetail):
    def before_delete(self, args, kwargs):
        """Hook to delete attachment from storage server before delete method"""
        delete_attachments_in_minio_by_related_object_id(DeviceSoftwareUpdateActionAttachment,
                                                         DeviceAttachment,
                                                         kwargs["id"])

    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}


class DeviceSoftwareUpdateActionAttachmentRelationship(ResourceRelationship):
    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}
