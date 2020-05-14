from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from project.api.models.baseModel import db
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.api.schemas.deviceSchema import DeviceSchema
from sqlalchemy.orm.exc import NoResultFound


class DeviceList(ResourceList):
    """

    """
    def query(self, view_kwargs):
        """

        :param view_kwargs:
        :return:
        """
        query_ = self.session.query(Device)
        if view_kwargs.get('id') is not None:
            try:
                self.session.query(Platform).filter_by(
                    id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'},
                                     "Platform: {} not found".format(
                                         view_kwargs['id']))
            else:
                query_ = query_.join(Platform).filter(
                    Platform.id == view_kwargs['id'])
        return query_

    def before_create_object(self, data, view_kwargs):
        """

        :param data:
        :param view_kwargs:
        :return:
        """
        if view_kwargs.get('id') is not None:
            platform = self.session.query(Platform).filter_by(
                id=view_kwargs['id']).one()
            data['platform_id'] = platform.id

    schema = DeviceSchema
    data_layer = {'session': db.session,
                  'model': Device,
                  'methods': {'query': query,
                              'before_create_object': before_create_object}}
