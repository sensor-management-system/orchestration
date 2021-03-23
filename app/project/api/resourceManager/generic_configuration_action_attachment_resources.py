from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.generic_action_attachments import GenericConfigurationActionAttachment
from ..schemas.generic_action_attachment_schema import (
    GenericConfigurationActionAttachmentSchema,
)
from ..token_checker import token_required


class GenericConfigurationActionAttachmentList(ResourceList):
    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}


class GenericConfigurationActionAttachmentDetail(ResourceDetail):
    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}


class GenericConfigurationActionAttachmentRelationship(ResourceRelationship):
    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}
