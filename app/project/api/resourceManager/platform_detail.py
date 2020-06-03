from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.resourceManager.base_resource import BaseResourceDetail
from project.api.schemas.platform_schema import PlatformSchema


class PlatformDetail(BaseResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete an Event
    """

    def before_get_object(self, view_kwargs):
        """
        before get method to get the platform id to fetch details
        :param view_kwargs:
        :return:
        """
        super().query_an_object(kwargs=view_kwargs, o=Platform)

    schema = PlatformSchema
    data_layer = {'session': db.session,
                  'model': Platform,
                  'methods': {'before_get_object': before_get_object}}
