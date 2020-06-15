from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.resourceManager.base_resource import BaseResourceDetail
from project.api.schemas.device_schema import DeviceSchema


class DeviceDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete a Device
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get('contact_id') is not None:
            BaseResourceDetail.query_an_object(view_kwargs, 'contact')

    schema = DeviceSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Device,
                  'methods': {'before_get_object': before_get_object}}
