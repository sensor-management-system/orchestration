import os

from ..models.contact_role import PlatformContactRole
from ...frj_csv_export.resource import ResourceList
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models.base_model import db
from ..models.platform import Platform
from ..resourceManager.base_resource import add_contact_to_object, add_created_by_id
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required


class PlatformList(ResourceList):
    """
    PlatformList class for creating a platformSchema
    only POST and GET method allowed
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
        Automatically add the created user to object contacts.
        Also add the owner to contact role.

        :param result:
        :return:
        """

        result_id = result[0]["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=result_id).first()
        contact = add_contact_to_object(platform)
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = PlatformContactRole(
            contact_id=contact.id,
            platform_id=platform.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        db.session.add(contact_role)
        db.session.commit()

        return result

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
        },
    }
