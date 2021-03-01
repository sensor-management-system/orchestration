from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.frj_csv_export.resource import ResourceList

from project.api.models.generic_action_attachments import GenericPlatformActionAttachment
from project.api.schemas.generic_action_attachment_schema import \
    GenericPlatformActionAttachmentSchema


class GenericPlatformActionAttachmentList(ResourceList):
    schema = GenericPlatformActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": GenericPlatformActionAttachment
    }


class GenericPlatformActionAttachmentDetail(ResourceDetail):
    schema = GenericPlatformActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": GenericPlatformActionAttachment
    }


class GenericPlatformActionAttachmentRelationship(ResourceRelationship):
    schema = GenericPlatformActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": GenericPlatformActionAttachment
    }
