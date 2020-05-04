from flask_rest_jsonapi import ResourceList

from project.api.models.baseModel import db
from project.api.models.event import Event
from project.api.schemas.eventSchema import EventSchema


class EventList(ResourceList):
    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event}