from project.api.models.base_model import db
from project.api.models.properties import Properties
from project.api.resourceManager.base_resource import BaseResourceDetail
from project.api.schemas.properties_schema import PropertiesSchema


class PropertiesDetail(BaseResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Platform
    """

    def before_get_object(self, view_kwargs):
        """
        before get method to get the Properties id to fetch details
        :param view_kwargs:
        :return:
        """
        super().query_an_object(kwargs=view_kwargs, o=Properties)

    schema = PropertiesSchema
    data_layer = {'session': db.session,
                  'model': Properties,
                  'methods': {'before_create_object': before_get_object}}
