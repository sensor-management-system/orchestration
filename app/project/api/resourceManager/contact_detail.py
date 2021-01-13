from flask_rest_jsonapi import ResourceDetail

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema
from project.api.token_checker import token_required


class ContactDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Contact
    """

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Contact,
    }
