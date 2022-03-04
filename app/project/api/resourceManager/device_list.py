from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..helpers.errors import BadRequestError
from ...api.auth.permission_utils import (
    get_collection_with_permissions,
    set_default_permission_view_to_internal_if_not_exists_or_all_false,
)
from ..models.base_model import db
from ..models.device import Device
from ..resourceManager.base_resource import add_contact_to_object
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required

from ...frj_csv_export.resource import ResourceList


class DeviceList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
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
            "after_get_collection": after_get_collection,
        },
    }
