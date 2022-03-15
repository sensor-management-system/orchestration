"""Device list resource."""

from ...api.auth.permission_utils import (
    get_es_query_with_permissions,
    get_query_with_permissions,
    set_default_permission_view_to_internal_if_not_exists_or_all_false,
)
from ...frj_csv_export.resource import ResourceList
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models.base_model import db
from ..models.device import Device
from ..resourceManager.base_resource import add_contact_to_object
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required


class DeviceList(ResourceList):
    """
    Resource for the device list endpoint.

    Supports GET (list) & POST (create) methods.
    """

    def query(self, view_kwargs):
        """
        Filter for what the user is allowed to query.

        :param view_kwargs:
        :return: queryset
        """
        return get_query_with_permissions(self.model)

    def es_query(self, view_kwargs):
        """
        Return the elasticsearch filter for the query.

        Should return the same set as query, but using
        the elasticsearch fields.
        """
        return get_es_query_with_permissions()

    def before_create_object(self, data, *args, **kwargs):
        """
        Set the visibility of the object (internal of nothing else is given).

        :param data: data of the request (as dict)
        :param args:
        :param kwargs:
        :return: None
        """
        # Will modify the data inplace.
        set_default_permission_view_to_internal_if_not_exists_or_all_false(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts.

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
            "query": query,
            "es_query": es_query,
        },
    }
