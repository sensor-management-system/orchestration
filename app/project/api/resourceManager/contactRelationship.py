from flask_rest_jsonapi import ResourceRelationship

from project.api.models.baseModel import db
from project.api.models.contact import Contact
from project.api.schemas.contactSchema import ContactSchema


class ContactRelationship(ResourceRelationship):
    schema = ContactSchema
    data_layer = {'session': db.session,
                  'model': Contact}