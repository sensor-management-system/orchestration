from flask_rest_jsonapi import ResourceRelationship

from ..models.base_model import db
from ..models.contact import Contact
from ..schemas.contact_schema import ContactSchema
from ..token_checker import token_required


class ContactRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Contact and other objects.
    """

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Contact}
