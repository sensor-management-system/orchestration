from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_action_attachments import GenericDeviceActionAttachment
from project.api.schemas.generic_action_attachment_schema import (
    GenericDeviceActionAttachmentSchema,
)
from project.frj_csv_export.resource import ResourceList


class GenericDeviceActionAttachmentList(ResourceList):
    schema = GenericDeviceActionAttachmentSchema
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}


class GenericDeviceActionAttachmentDetail(ResourceDetail):
    schema = GenericDeviceActionAttachmentSchema
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}


class GenericDeviceActionAttachmentRelationship(ResourceRelationship):
    schema = GenericDeviceActionAttachmentSchema
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}
