from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.models.event import Event
from project.api.schemas.event_schema import EventSchema


class EventList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Events or create one.
    """
    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event}
