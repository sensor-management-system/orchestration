from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from .base_resource import delete_attachments_in_minio_by_related_object_id
from ..models import ConfigurationAttachment
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
    def before_delete(self, args, kwargs):
        """Hook to delete attachment from storage server before delete method"""
        delete_attachments_in_minio_by_related_object_id(GenericConfigurationActionAttachment,
                                                         ConfigurationAttachment, kwargs["id"])

    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}


class GenericConfigurationActionAttachmentRelationship(ResourceRelationship):
    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}
