from flask import request

from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed, UnauthorizedError
from ..services.idl_services import Idl


class UserInfo(ResourceList):
    """
    JSON API resource to retrieve information about a user.

    It gathers from the local database and the institute decoupling layer.
    User data will be found using the JWT token & the get_current_user function."""

    def get(self):
        """GET method to retrieve information gathered from database and
        Institute decoupling layer (IDL) from user subject.

        :return: Dict with user infos from database + IDL-groups.
        """
        if not request.user:
            raise UnauthorizedError("Login required")
        idl_groups = Idl().get_all_permission_groups_for_a_user(request.user.subject)
        data = {
            "data": {
                "type": "user",
                "id": request.user.id,
                "attributes": {
                    "admin": idl_groups.administrated_permission_groups
                    if idl_groups
                    else [],
                    "member": idl_groups.membered_permission_groups
                    if idl_groups
                    else [],
                    "active": request.user.active,
                    "is_superuser": request.user.is_superuser,
                },
            }
        }
        return data

    def post(self, *args, **kwargs):
        raise MethodNotAllowed("endpoint is readonly")
