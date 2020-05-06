from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound

from project.api.models.baseModel import db
from project.api.models.device import Device
from project.api.schemas.fieldSchema import FieldSchema
from project.api.models.field import Field
from sqlalchemy.orm.exc import NoResultFound


class FieldDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
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

    schema = FieldSchema
    data_layer = {'session': db.session,
                  'model': Field,
                  'methods': {'before_create_object': before_get_object}}
