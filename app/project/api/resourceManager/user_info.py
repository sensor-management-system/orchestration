from flask_jwt_extended import jwt_required, get_current_user

from ..helpers.errors import MethodNotAllowed
from ..services.idl_services import Idl
from ...frj_csv_export.resource import ResourceList


class UserInfo(ResourceList):
    """
    JSON API resource to retrieve information about a user.

    It gathers from the local database and the institute decoupling layer.
    User data will be found using the JWT token & the get_current_user function."""

    @jwt_required()
    def get(self):
        """GET method to retrieve information gathered from database and
        Institute decoupling layer (IDL) from user subject.

        :return: Dict with user infos from database + IDL-groups.
        """
        current_user = get_current_user()
        idl_groups = Idl().get_all_permission_groups(current_user.subject)
        data = {
            "data": {
                "type": "user",
                "id": current_user.id,
                "attributes": {
                    "admin": idl_groups.administrated_permission_groups
                    if idl_groups
                    else [],
                    "member": idl_groups.membered_permission_groups
                    if idl_groups
                    else [],
                    "active": current_user.active,
                    "is_superuser": current_user.is_superuser,
                },
            }
        }
        return data

    def post(self, *args, **kwargs):
        raise MethodNotAllowed("endpoint is readonly")
