from project.api.models.base_model import db
from project.api.models.event import Event
from project.api.resourceManager.base_resource import BaseResourceDetail
from project.api.schemas.event_schema import EventSchema


class EventDetail(BaseResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an Event and delete a Event
    """

    def before_get_object(self, view_kwargs):
        """
        before get method to get the event id to fetch details
        :param view_kwargs:
        :return:
        """
        super().query_an_object(kwargs=view_kwargs, o=Event)

    schema = EventSchema
    data_layer = {'session': db.session,
                  'model': Event,
                  'methods': {'before_create_object': before_get_object}}
