from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from project.api.models.base_model import db
from project.api.models.device_property import DeviceProperty
from project.api.schemas.device_property_schema import DevicePropertySchema
from project.api.token_checker import token_required
from sqlalchemy.orm.exc import NoResultFound


class DevicePropertyDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                _ = (
                    self.session.query(DeviceProperty)
                    .filter_by(id=view_kwargs["id"])
                    .one()
                )
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "Configuration_id"},
                    "Configuration: {} not found".format(view_kwargs["id"]),
                )

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
        "methods": {"before_get_object": before_get_object},
    }
