from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.generic_action_attachments import GenericDeviceActionAttachment
from ..schemas.generic_action_attachment_schema import (
    GenericDeviceActionAttachmentSchema,
)
from ..token_checker import token_required


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
