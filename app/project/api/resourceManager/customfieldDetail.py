from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound

from project.api.models.baseModel import db
from project.api.models.device import Device
from project.api.schemas.customfieldSchema import CustomFieldSchema
from project.api.models.customfield import CustomField
from sqlalchemy.orm.exc import NoResultFound


class CustomFieldDetail(ResourceDetail):
    """
    Custom Field detail class.
    """
    def before_get_object(self, view_kwargs):
        """
        before get method to get the field id to fetch details
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('device_id') is not None:
            try:
                device = self.session.query(Device).filter_by(
                    id=view_kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'},
                                     "Device: {} not found".format(
                                         view_kwargs['device_id']))
            else:
                if device.platform is not None:
                    view_kwargs['id'] = device.platform.id
                else:
                    view_kwargs['id'] = None

    schema = CustomFieldSchema
    data_layer = {'session': db.session,
                  'model': CustomField,
                  'methods': {'before_create_object': before_get_object}}
