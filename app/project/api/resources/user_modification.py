"""Resources to modify the current user."""

from flask import g

from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed, UnauthorizedError
from ..models import User
from ..models.base_model import db


class RevokeApikey(ResourceList):
    """Resource to allow the user to revoke the apikey - and to get a new one."""

    def get(self):
        """Get is not allowed."""
        raise MethodNotAllowed("Endpoint can only be used with POST method.")

    def post(self):
        """Take the user of the request set a new apikey & return it."""
        if not g.user:
            raise UnauthorizedError("Login required")
        g.user.apikey = User.generate_new_apikey()
        db.session.add(g.user)
        db.session.commit()

        response = {
            "data": {
                "type": "user",
                "id": str(g.user.id),
                "attributes": {"apikey": g.user.apikey},
            }
        }
        return response
