from ..auth.flask_openidconnect import open_id_connect
from ..helpers.errors import MethodNotAllowed
from ..models.permission_groups import permission_groups_to_list_of_jsonapi_dicts
from ...api.services.idl_services import get_permission_groups
from ...frj_csv_export.resource import ResourceList


class PermissionGroups(ResourceList):
    """
    List the Permission Groups in a json:api style.
    """

    def get(self, *args, **kwargs):
        """
        Retrieve a list of Permission Groups.

        :return: list of Permission Groups.
        """
        open_id_connect.verify_valid_access_token_in_request_and_set_user()
        data = permission_groups_to_list_of_jsonapi_dicts(get_permission_groups())
        response = {"data": data}
        response.update({"meta": {"count": len(data)}})
        return response

    def post(self, *args, **kwargs):
        raise MethodNotAllowed("Endpoint is readonly")
