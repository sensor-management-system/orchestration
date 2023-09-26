# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Login/logout related routes to put users into the session."""

from flask import Blueprint, g, request, session

from ..api.helpers.errors import AuthenticationFailedError, UnauthorizedError
from ..config import env
from ..extensions.instances import open_id_connect_auth_mechanism

login_routes = Blueprint(
    "login", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


@login_routes.route("/login/by-access-token", methods=["POST"])
def login_by_access_token():
    """
    Put the user in the session.

    Returns 204 if successful.
    """
    if "accesstoken" in request.values:
        access_token = request.values.get("accesstoken")
    elif "accesstoken" in request.json:
        access_token = request.json.get("accesstoken")

    user = open_id_connect_auth_mechanism.authenticate_by_authorization(access_token)
    if not user:
        raise AuthenticationFailedError("No valid token")
    else:
        session["user_id"] = user.id

    return ("", 204)


@login_routes.route("logout", methods=["POST"])
def logout():
    """
    Remove the user from the session.

    Returns 204 if successful.
    """
    if not g.user:
        raise UnauthorizedError("Authentication required.")
    if "user_id" in session:
        session.pop("user_id", None)
    return ("", 204)
