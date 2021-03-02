"""Module for hte customfield list resource."""
from flask_rest_jsonapi import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.customfield import Customfield
from project.api.models.device import Device
from project.api.schemas.customfield_schema import CustomfieldSchema
from project.api.token_checker import token_required


class CustomfieldList(ResourceList):
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
        query_ = self.session.query(Customfield)
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
                query_ = query_.filter(Customfield.device_id == device_id)
        return query_

    schema = CustomfieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Customfield,
        "methods": {
            "query": query,
        },
    }
