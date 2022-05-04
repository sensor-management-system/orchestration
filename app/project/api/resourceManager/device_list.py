import os

from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models.base_model import db
from ..models.contact_role import DeviceContactRole
from ..models.device import Device
from ..resourceManager.base_resource import add_contact_to_object, add_created_by_id
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


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
        add_created_by_id(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts
        Also add the owner to contact role.

        :param result:
        :return:
        """

        result_id = result[0]["data"]["id"]
        device = db.session.query(Device).filter_by(id=result_id).first()
        contact = add_contact_to_object(device)
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = DeviceContactRole(
            contact_id=contact.id,
            device_id=device.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        db.session.add(contact_role)
        db.session.commit()

        return result

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
        "class": EsSqlalchemyDataLayer,
        "methods": {"before_create_object": before_create_object},
    }
