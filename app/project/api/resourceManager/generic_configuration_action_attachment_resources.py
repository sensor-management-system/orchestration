from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.generic_action_attachments import GenericConfigurationActionAttachment
from ..schemas.generic_action_attachment_schema import (
    GenericConfigurationActionAttachmentSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class GenericConfigurationActionAttachmentList(ResourceList):
    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}


class GenericConfigurationActionAttachmentDetail(ResourceDetail):
    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericConfigurationActionAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}


class GenericConfigurationActionAttachmentRelationship(ResourceRelationship):
    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}
