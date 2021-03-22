"""Module for hte customfield list resource."""
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..models.base_model import db
from ..models.customfield import CustomField
from ..models.device import Device
from ..schemas.customfield_schema import CustomFieldSchema
from ..token_checker import token_required


class CustomFieldList(ResourceList):
    """
    List resource for custom fields.

    Provides get and post methods to retrieve
    a list of custom fields or to create a new one.
    """

    def query(self, view_kwargs):
        """
        Query the data from the database.

        Normally it should query all the customfields.
        However, if we give a device_id with a url like
        /devices/<device_id>/customfields
        we want to filter according to them.
        """
        query_ = self.session.query(CustomField)
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(CustomField.device_id == device_id)
        return query_

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
        "methods": {
            "query": query,
        },
    }
