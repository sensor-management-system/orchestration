from flask import g

from ...extensions.instances import idl
from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed, UnauthorizedError


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
        if not g.user:
            raise UnauthorizedError("Login required")
        idl_groups = idl.get_all_permission_groups_for_a_user(g.user.subject)
        data = {
            "data": {
                "type": "user",
                "id": g.user.id,
                "attributes": {
                    "admin": idl_groups.administrated_permission_groups
                    if idl_groups
                    else [],
                    "member": idl_groups.membered_permission_groups
                    if idl_groups
                    else [],
                    "active": g.user.active,
                    "is_superuser": g.user.is_superuser,
                },
            }
        }
        return data

    def post(self, *args, **kwargs):
        raise MethodNotAllowed("endpoint is readonly")
