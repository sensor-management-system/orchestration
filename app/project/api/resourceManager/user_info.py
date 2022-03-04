from ..auth.flask_openidconnect import open_id_connect
from ..helpers.errors import MethodNotAllowed
from ..services.idl_services import Idl
from ...frj_csv_export.resource import ResourceList


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
        open_id_connect.verify_valid_access_token_in_request_and_set_user()
        current_user = open_id_connect.get_current_user()
        idl_groups = Idl().get_all_permission_groups_for_a_user(current_user.subject)
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
