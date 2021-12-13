"""Module for the device property list resource."""
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_collection_with_permissions_for_related_objects
from ..models.base_model import db
from ..models.device import Device
from ..models.device_property import DeviceProperty
from ..schemas.device_property_schema import DevicePropertySchema
from ..token_checker import token_required


class DevicePropertyList(ResourceList):
    """
    List resource for device properties.

    Provides get and post methods to retrieve
    a collection of device properties or create one.
    """

    def after_get_collection(self, collection, qs, view_kwargs):
        """Take the intersection between requested collection and
        what the user allowed querying.

        :param collection:
        :param qs:
        :param view_kwargs:
        :return:
        """

        return get_collection_with_permissions_for_related_objects(
            self.model, collection
        )

    def query(self, view_kwargs):
        """
        Query all the entries from the database.

        Also handle cases to search for all the device
        properties of a specific device.
        """
        query_ = self.session.query(DeviceProperty)
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",}, "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceProperty.device_id == device_id)
        return query_

    schema = DevicePropertySchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceProperty,
        "methods": {"query": query, "after_get_collection": after_get_collection},
    }
