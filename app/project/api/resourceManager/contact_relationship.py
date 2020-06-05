from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema
from project.api.token_checker import token_required


class ContactRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Contact and other objects.
    """
    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Contact}
