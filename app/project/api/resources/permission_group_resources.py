from ...extensions.idl.models import permission_group
from ...extensions.instances import idl
from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed


class PermissionGroups(ResourceList):
    """
    List the Permission Groups in a json:api style.
    """

    def get(self, *args, **kwargs):
        """
        Retrieve a list of Permission Groups.

        :return: list of Permission Groups.
        """
        data = permission_group.permission_groups_to_list_of_jsonapi_dicts(
            idl.get_permission_groups()
        )
        response = {"data": data}
        response.update({"meta": {"count": len(data)}})
        return response

    def post(self, *args, **kwargs):
        raise MethodNotAllowed("Endpoint is readonly")
