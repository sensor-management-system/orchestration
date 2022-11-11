"""Resource classes for the user info endpoint."""

from flask import g

from ...extensions.instances import idl
from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed, UnauthorizedError
from ..models import User
from ..models.base_model import db


class UserInfo(ResourceList):
    """
    JSON API resource to retrieve information about a user.

    It gathers from the local database and the institute decoupling layer.
    User data will be found using the auth mechanism.
    """

    def get(self):
        """
        GET method to retrieve information for a user.

        It is gathered from database and
        Institute decoupling layer (IDL) from user subject.

        :return: Dict with user infos from database + IDL-groups.
        """
        if not g.user:
            raise UnauthorizedError("Login required")
        idl_groups = idl.get_all_permission_groups_for_a_user(g.user.subject)

        if not g.user.apikey:
            g.user.apikey = User.generate_new_apikey()
            db.session.add(g.user)
            db.session.commit()
        data = {
            "data": {
                "type": "user",
                "id": str(g.user.id),
                "attributes": {
                    "admin": idl_groups.administrated_permission_groups
                    if idl_groups
                    else [],
                    "member": idl_groups.membered_permission_groups
                    if idl_groups
                    else [],
                    "active": g.user.active,
                    "is_superuser": g.user.is_superuser,
                    "apikey": g.user.apikey,
                },
                "relationships": {
                    "contact": {
                        "data": {"type": "contact", "id": str(g.user.contact_id)}
                    }
                },
            },
        }
        return data

    def post(self, *args, **kwargs):
        """Don't allow post requests."""
        raise MethodNotAllowed("endpoint is readonly")
