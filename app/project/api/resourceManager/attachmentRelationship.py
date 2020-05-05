from flask_rest_jsonapi import ResourceRelationship

from project.api.models.baseModel import db
from project.api.schemas.attachmentSchema import AttachmentSchema
from project.api.models.attachment import Attachment


class AttachmentRelationship(ResourceRelationship):
    schema = AttachmentSchema
    data_layer = {'session': db.session,
                  'model': Attachment}