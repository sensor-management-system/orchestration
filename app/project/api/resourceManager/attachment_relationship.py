from flask_rest_jsonapi import ResourceRelationship
from project.api.models.attachment import Attachment
from project.api.models.base_model import db
from project.api.schemas.attachment_schema import AttachmentSchema
from project.api.token_checker import token_required


class AttachmentRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Attachment and other objects.
    """
    schema = AttachmentSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Attachment}
