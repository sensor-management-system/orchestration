from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.event import Event
from project.api.schemas.event_schema import EventSchema
from project.api.token_checker import token_required


class EventDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an Event and delete a Event
    """

    schema = EventSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Event}
