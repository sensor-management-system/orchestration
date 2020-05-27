from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.schemas.attachment_schema import AttachmentSchema
from project.api.models.attachment import Attachment


class AttachmentList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Attachment or create one.
    """
    schema = AttachmentSchema
    data_layer = {'session': db.session,
                  'model': Attachment}
