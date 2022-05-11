from flask_rest_jsonapi import ResourceRelationship

from ..helpers.errors import MethodNotAllowed
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


class ContactRelationshipReadOnly(ContactRelationship):
    """A readonly relationship endpoint for contacts."""

    def before_post(self, args, kwargs, json_data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_patch(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        raise MethodNotAllowed("This endpoint is readonly!")
