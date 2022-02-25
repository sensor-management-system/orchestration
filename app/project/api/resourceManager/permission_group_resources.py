from flask_jwt_extended import jwt_required

from ..helpers.errors import MethodNotAllowed
from ..models.permission_groups import permission_groups_to_list_of_jsonapi_dicts
from ...api.services.idl_services import get_permission_groups
from ...frj_csv_export.resource import ResourceList


class PermissionGroups(ResourceList):
    """
    List the Permission Groups in a json:api style.
    """

    @jwt_required()
    def get(self, *args, **kwargs):
        """
        Retrieve a list of Permission Groups.

        :return: list of Permission Groups.
        """
        data = permission_groups_to_list_of_jsonapi_dicts(get_permission_groups())
        response = {"data": data}
        response.update({"meta": {"count": len(data)}})
        return response

    def post(self, *args, **kwargs):
        raise MethodNotAllowed("Endpoint is readonly")
