"""Login/logout related routes to put users into the session."""

from flask import Blueprint, g, redirect, render_template, request, session, url_for

from ...config import env
from ...extensions.instances import open_id_connect_auth_mechanism

login_routes = Blueprint(
    "login", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


@login_routes.route("/login/by-access-token", methods=["GET", "POST"])
def login_by_access_token():
    """
    Show login form for usage with the access token.

    Set the user into the session in case we have a valid access token.
    """
    error = None
    if request.method == "POST":
        access_token = request.form.get("accesstoken")
        user = open_id_connect_auth_mechanism.authenticate_by_authorization(
            access_token
        )
        if not user:
            error = "No valid access token."
        else:
            session["user_id"] = user.id
            return redirect(url_for("login.show_login_success"))

    return render_template("auth_pages/login_by_access_token.html", error=error)


@login_routes.route("login/success", methods=["GET"])
def show_login_success():
    """Show the message that the login was successful."""
    if not g.user:
        return redirect(url_for("login.login_required"))
    return render_template("auth_pages/login_success.html")


@login_routes.route("login-required")
def login_required():
    """Show the message that a login is required to access the page."""
    return render_template("auth_pages/login_required.html")


@login_routes.route("logout", methods=["GET", "POST"])
def logout():
    """
    Show a button to logout.

    Remove the user from the session for the post request.
    """
    if not g.user:
        return redirect(url_for("login.login_required"))
    if request.method == "POST":
        session.pop("user_id", None)
        return redirect(url_for("login.show_logout_success"))

    return render_template("auth_pages/logout.html")


@login_routes.route("logout/success", methods=["GET"])
def show_logout_success():
    """Show the message that the logout was successful."""
    return render_template("auth_pages/logout_success.html")
