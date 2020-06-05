from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.resourceManager.base_resource import BaseResourceDetail
from project.api.schemas.device_schema import DeviceSchema
from project.api.token_checker import token_required


class DeviceDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete a Device
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get('event_id') is not None:
            BaseResourceDetail.query_an_object(view_kwargs, 'event')
        if view_kwargs.get('contact_id') is not None:
            BaseResourceDetail.query_an_object(view_kwargs, 'contact')
        if view_kwargs.get('properties_id') is not None:
            BaseResourceDetail.query_an_object(view_kwargs, 'properties')
        if view_kwargs.get('attachments_id') is not None:
            BaseResourceDetail.query_an_object(view_kwargs, 'attachments')

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Device,
                  'methods': {'before_get_object': before_get_object}}
