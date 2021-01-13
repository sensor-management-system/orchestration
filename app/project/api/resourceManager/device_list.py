from flask_rest_jsonapi import ResourceList

from project.api.datalayers.esalchemy import EsSqlalchemyDataLayer
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.resourceManager.base_resource import (add_contact_to_object,
                                                       add_create_by_id)
from project.api.schemas.device_schema import DeviceSchema
from project.api.token_checker import token_required


class DeviceList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    def before_create_object(self, data, *args, **kwargs):
        """
        Use jwt to add user id to dataset
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        add_create_by_id(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts
        :param result:
        :return:
        """

        result_id = result[0]["data"]["id"]
        d = db.session.query(Device).filter_by(id=result_id).first()
        add_contact_to_object(d)

        return result

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
        },
    }
