from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models.base_model import db
from ..models.platform import Platform
from ..resourceManager.base_resource import (
    add_contact_to_object,
    add_created_by_id,
    set_object_query, validate_object_state,
)
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class PlatformList(ResourceList):
    """
    PlatformList class for creating a platformSchema
    only POST and GET method allowed
    """

    def query(self, view_kwargs):
        """
        query method To show only allowed objects.

        :param view_kwargs:
        :return:
        """
        query_ = set_object_query(Platform)
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """
        Use jwt to add user id to dataset
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        add_created_by_id(data)
        validate_object_state(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts
        :param result:
        :return:
        """

        result_id = result[0]["data"]["id"]
        d = db.session.query(Platform).filter_by(id=result_id).first()
        add_contact_to_object(d)

        return result

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
        "class": EsSqlalchemyDataLayer,
        "methods": {"before_create_object": before_create_object, "query": query},
    }
