from flask_rest_jsonapi import ResourceList
from project.api.models.attachment import Attachment
from project.api.models.base_model import db
from project.api.schemas.attachment_schema import AttachmentSchema
from project.api.token_checker import token_required


class AttachmentList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Attachment or create one.
    """
    schema = AttachmentSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Attachment}
