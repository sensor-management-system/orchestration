from project.api.models.base_model import db
from project.api.models.customfield import CustomField
from project.api.resourceManager.base_resource import BaseResourceDetail
from project.api.schemas.customfield_schema import CustomFieldSchema


class CustomFieldDetail(BaseResourceDetail):
    """
    Custom Field detail class.
    """

    def before_get_object(self, view_kwargs):
        """
        before get method to get the field id to fetch details
        :param view_kwargs:
        :return:
        """
        super().query_an_object(kwargs=view_kwargs, o=CustomField)

    schema = CustomFieldSchema
    data_layer = {'session': db.session,
                  'model': CustomField,
                  'methods': {'before_create_object': before_get_object}}
