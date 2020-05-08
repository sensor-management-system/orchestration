from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from project.api.models.baseModel import db
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.api.schemas.platformSchema import PlatformSchema
from sqlalchemy.orm.exc import NoResultFound


class PlatformDetail(ResourceDetail):
    """
    Platform details class
    """
    def before_get_object(self, view_kwargs):
        """
        before get method to get the platform id to fetch details
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('device_id') is not None:
            try:
                device = self.session.query(Device).filter_by(
                    id=view_kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'},
                                     "Platform: {} not found".format(
                                         view_kwargs['device_id']))
            else:
                if device.platform is not None:
                    view_kwargs['id'] = device.platform.id
                else:
                    view_kwargs['id'] = None

    schema = PlatformSchema
    data_layer = {'session': db.session,
                  'model': Platform,
                  'methods': {'before_get_object': before_get_object}}
