from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from project.api.models.device import Device
from sqlalchemy.orm.exc import NoResultFound


class BaseResourceDetail(ResourceDetail):
    """
    Base Resource detail
    """

    def query_an_object(self, o, kwargs):
        """

        :param kwargs:
        :return:
        """
        if kwargs.get('device_id') is not None:
            try:
                device = self.session.query(Device).filter_by(
                    id=kwargs['device_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'},
                                     "Device: {} not found".format(
                                         kwargs['device_id']))
            else:
                if device.o is not None:
                    kwargs['id'] = device.o.id
                else:
                    kwargs['id'] = None
