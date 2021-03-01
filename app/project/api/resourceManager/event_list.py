from project.api.models.base_model import db
from project.api.models.event import Event
from project.api.schemas.event_schema import EventSchema
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


class EventList(ResourceList):
    """
    Class that provides get and post methods to
    retrieve a collection of Events or create one.
    """

    schema = EventSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Event}
