from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.schemas.device_schema import DeviceSchema


class DeviceDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete a Device
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get('id') is not None:
            try:
                _ = self.session.query(Device).filter_by(
                    id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'device_id'},
                                     "Device: {} not found".format(view_kwargs['id']))

    schema = DeviceSchema
    # decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
        'methods': {'before_get_object': before_get_object}
    }
