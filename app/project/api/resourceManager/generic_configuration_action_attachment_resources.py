from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.frj_csv_export.resource import ResourceList

from project.api.models.generic_action_attachments import GenericConfigurationActionAttachment
from project.api.schemas.generic_action_attachment_schema import \
    GenericConfigurationActionAttachmentSchema


class GenericConfigurationActionAttachmentList(ResourceList):
    schema = GenericConfigurationActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationActionAttachment
    }


class GenericConfigurationActionAttachmentDetail(ResourceDetail):
    schema = GenericConfigurationActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationActionAttachment
    }


class GenericConfigurationActionAttachmentRelationship(ResourceRelationship):
    schema = GenericConfigurationActionAttachmentSchema
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationActionAttachment
    }
