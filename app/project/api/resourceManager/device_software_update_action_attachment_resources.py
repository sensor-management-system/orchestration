from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.software_update_action_attachments import (
    DeviceSoftwareUpdateActionAttachment,
)
from project.api.schemas.software_update_action_attachment_schema import (
    DeviceSoftwareUpdateActionAttachmentSchema,
)
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


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
