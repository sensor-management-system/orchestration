from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.event import Event
from project.api.schemas.event_schema import EventSchema
from project.api.token_checker import token_required


class EventRelationship(ResourceRelationship):
    """
    Class that provides get, post, patch and delete
    methods to get relationships, create relationships,
    update and delete between Events and other objects.
    """

    schema = EventSchema
    # decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Event,
    }
