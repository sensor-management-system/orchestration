from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.software_update_action_attachments import (
    DeviceSoftwareUpdateActionAttachment,
)
from ..schemas.software_update_action_attachment_schema import (
    DeviceSoftwareUpdateActionAttachmentSchema,
)
from ..token_checker import token_required


class DeviceSoftwareUpdateActionAttachmentList(ResourceList):
    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}


class DeviceSoftwareUpdateActionAttachmentDetail(ResourceDetail):
    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}


class DeviceSoftwareUpdateActionAttachmentRelationship(ResourceRelationship):
    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}
