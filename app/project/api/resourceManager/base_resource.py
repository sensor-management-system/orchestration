from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound
from project.api.models.device import Device


class BaseResourceDetail(ResourceDetail):
    """
    Base Resource detail
    """

    def query_an_object(self, kwargs, object_):
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
                o = self.session.query(object_).filter_by(
                    id=kwargs['id']).one()
                if device[o] is not None:
                    kwargs['id'] = device[o].id
                else:
                    kwargs['id'] = None
