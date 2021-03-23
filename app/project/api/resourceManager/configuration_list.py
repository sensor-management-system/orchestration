from ...frj_csv_export.resource import ResourceList
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models.base_model import db
from ..models.configuration import Configuration
from ..resourceManager.base_resource import add_contact_to_object, add_created_by_id
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import token_required


class ConfigurationList(ResourceList):
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
        :param result:
        :return:
        """

        result_id = result[0]["data"]["id"]
        d = db.session.query(Configuration).filter_by(id=result_id).first()
        add_contact_to_object(d)

        return result

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
        },
    }
