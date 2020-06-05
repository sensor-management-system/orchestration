from flask_rest_jsonapi import ResourceDetail
from project.api.models.attachment import Attachment
from project.api.models.base_model import db
from project.api.schemas.attachment_schema import AttachmentSchema
from project.api.token_checker import token_required


class AttachmentDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete an Attachment
    """

    schema = AttachmentSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Attachment}
