from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ...api.auth.permission_utils import (
    get_collection_with_permissions,
    set_default_permission_view_to_internal_if_not_exists_or_all_false,
)
from ..models.base_model import db
from ..models.platform import Platform
from ..resourceManager.base_resource import add_contact_to_object
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class PlatformList(ResourceList):
    """
    PlatformList class for creating a platformSchema
    only POST and GET method allowed
    """

    def after_get_collection(self, collection, qs, view_kwargs):
        """Take the intersection between requested collection and
        what the user allowed querying.

        :param collection:
        :param qs:
        :param view_kwargs:
        :return:
        """

        return get_collection_with_permissions(self.model, collection, qs, view_kwargs)

    def after_get(self, result):
        result.update({"meta": {"count": len(result["data"])}})
        return result

    def before_create_object(self, data, *args, **kwargs):
        """
        Use jwt to add user id to dataset
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        set_default_permission_view_to_internal_if_not_exists_or_all_false(data)

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
        "methods": {
            "before_create_object": before_create_object,
            "after_get_collection": after_get_collection,
        },
    }
