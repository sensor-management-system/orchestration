from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_action_attachments import (
    GenericPlatformActionAttachment,
)
from project.api.schemas.generic_action_attachment_schema import (
    GenericPlatformActionAttachmentSchema,
)
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


class GenericPlatformActionAttachmentList(ResourceList):
    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}


class GenericPlatformActionAttachmentDetail(ResourceDetail):
    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}


class GenericPlatformActionAttachmentRelationship(ResourceRelationship):
    schema = GenericPlatformActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericPlatformActionAttachment}
