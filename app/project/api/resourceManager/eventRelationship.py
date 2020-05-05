from flask_rest_jsonapi import ResourceRelationship

from project.api.models.baseModel import db
from project.api.models.event import Event
from project.api.schemas.eventSchema import EventSchema


class EventRelationship(ResourceRelationship):
    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event}
