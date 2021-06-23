from flask_rest_jsonapi import ResourceDetail

from ..models.base_model import db
from ..models.event import Event
from ..schemas.event_schema import EventSchema
from ..token_checker import token_required


class EventDetail(ResourceDetail):
    """
    Class that provides get, patch and delete methods
    to retrieve details of an object, updates an object
    and deletes an Event.
    """

    schema = EventSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Event,
    }
