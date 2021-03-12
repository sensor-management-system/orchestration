from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_action_attachments import GenericDeviceActionAttachment
from project.api.schemas.generic_action_attachment_schema import (
    GenericDeviceActionAttachmentSchema,
)
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


class GenericDeviceActionAttachmentList(ResourceList):
    schema = GenericDeviceActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}


class GenericDeviceActionAttachmentDetail(ResourceDetail):
    schema = GenericDeviceActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}


class GenericDeviceActionAttachmentRelationship(ResourceRelationship):
    schema = GenericDeviceActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericDeviceActionAttachment}
