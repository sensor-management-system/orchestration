from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import check_if_object_not_found
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
    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceSoftwareUpdateActionAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}


class DeviceSoftwareUpdateActionAttachmentRelationship(ResourceRelationship):
    schema = DeviceSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": DeviceSoftwareUpdateActionAttachment}
