from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.generic_action_attachments import GenericPlatformActionAttachment
from ..schemas.generic_action_attachment_schema import (
    GenericPlatformActionAttachmentSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class GenericPlatformActionAttachmentList(ResourceList):
    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}


class GenericPlatformActionAttachmentDetail(ResourceDetail):
    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericPlatformActionAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}


class GenericPlatformActionAttachmentRelationship(ResourceRelationship):
    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}
