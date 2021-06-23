from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.event import Event
from ..schemas.event_schema import EventSchema
from ..token_checker import token_required


class EventList(ResourceList):
    """
    Class that provides get and post methods to
    retrieve a collection of Events or create one.
    """

    schema = EventSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Event}
