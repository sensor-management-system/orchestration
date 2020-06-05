from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.event import Event
from project.api.schemas.event_schema import EventSchema


class EventDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an Event and delete a Event
    """

    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event}
