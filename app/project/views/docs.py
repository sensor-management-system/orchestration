"""Views for the OpenAPI specification."""

from flask import Blueprint, current_app, render_template

from ..config import env

docs_routes = Blueprint(
    "docs", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


@docs_routes.route("/swagger", methods=["GET"])
def swagger():
    """Render the swagger UI."""
    return render_template("swaggerui.html")


@docs_routes.route("/openapi", methods=["GET"])
def openapi():
    """Render the OpenAPI UI."""
    return render_template(
        "openapi.html",
        client_id=current_app.config["PKCE_CLIENT_ID"],
        scopes=current_app.config["PKCE_SCOPES"],
        redirect_url=f'{current_app.config["SMS_BACKEND_URL"]}/login-callback',
    )


@docs_routes.route("/login-callback", methods=["GET"])
def openapi_callback():
    """Provide the login callback for the OpenAPI OIDC Login mechanism."""
    return render_template("auth_pages/oauth2-redirect.html")


@docs_routes.route("/openapi.json", methods=["GET"])
def openapi_json():
    """Return the OpenAPI specification in json."""
    # We parameterize this a little bit in order to provide the docs
    # for the specific instance of the SMS.
    #
    # We reuse the url prefix here, so we fill the base url that points
    # to all the other routes as well.
    url = docs_routes.url_prefix
    description = "SMS Instance"
    servers = [
        {
            "url": url,
            "description": description,
        },
    ]
    token_endpoint = current_app.config["OIDC_TOKEN_ENDPOINT"]
    authorization_endpoint = current_app.config["OIDC_AUTHORIZATION_ENDPOINT"]
    result = render_template(
        "openapi.json",
        servers=servers,
        token_endpoint=token_endpoint,
        authorization_endpoint=authorization_endpoint,
    )
    return result, 200, {"Content-type": "application/json"}
