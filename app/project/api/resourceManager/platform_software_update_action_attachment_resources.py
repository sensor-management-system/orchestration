from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import check_if_object_not_found
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
    schema = PlatformSoftwareUpdateActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateActionAttachment,
    }


class PlatformSoftwareUpdateActionAttachmentDetail(ResourceDetail):
    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformSoftwareUpdateActionAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

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
