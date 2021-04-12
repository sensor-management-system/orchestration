from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import delete_attachments_in_minio_by_related_object_id
from ..models import DeviceAttachment
from ..models.base_model import db
from ..models.generic_action_attachments import GenericDeviceActionAttachment
from ..schemas.generic_action_attachment_schema import (
    GenericDeviceActionAttachmentSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class GenericDeviceActionAttachmentList(ResourceList):
    schema = GenericDeviceActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}


class GenericDeviceActionAttachmentDetail(ResourceDetail):
    def before_delete(self, args, kwargs):
        """Hook to delete attachment from storage server before delete method"""
        delete_attachments_in_minio_by_related_object_id(GenericDeviceActionAttachment,
                                                         DeviceAttachment,
                                                         kwargs["id"])

    schema = GenericDeviceActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}


class GenericDeviceActionAttachmentRelationship(ResourceRelationship):
    schema = GenericDeviceActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}
