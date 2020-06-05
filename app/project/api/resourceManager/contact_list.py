from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema
from project.api.token_checker import token_required


class ContactList(ResourceList):
    """
    provides get and post methods to retrieve
     a collection of Contacts or create one.
    """
    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Contact}
