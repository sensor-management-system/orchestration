from flask_rest_jsonapi import ResourceList

from project.api.models.baseModel import db
from project.api.models.contact import Contact
from project.api.schemas.contactSchema import ContactSchema


class ContactList(ResourceList):
    schema = ContactSchema
    data_layer = {'session': db.session,
                  'model': Contact}
