from flask_rest_jsonapi import ResourceList

from project.api.models.baseModel import db
from project.api.schemas.attachmentSchema import AttachmentSchema
from project.api.models.attachment import Attachment


class AttachmentList(ResourceList):
    schema = AttachmentSchema
    data_layer = {'session': db.session,
                  'model': Attachment}