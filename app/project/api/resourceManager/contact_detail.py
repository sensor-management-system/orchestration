from flask_rest_jsonapi import ResourceDetail

from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.contact import Contact
from ..schemas.contact_schema import ContactSchema
from ..token_checker import token_required


class ContactDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Contact
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if contact not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Contact,
    }
