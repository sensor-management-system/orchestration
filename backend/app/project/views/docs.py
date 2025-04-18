# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Views for the OpenAPI specification."""

import importlib
import json
import pkgutil

from flask import Blueprint, current_app, render_template, url_for

from ..config import env
from . import openapi_parts

docs_routes = Blueprint(
    "docs", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


@docs_routes.route("/openapi", methods=["GET"])
def openapi():
    """Render the OpenAPI UI."""
    redirect_url = url_for("docs.openapi_callback", _external=True)
    return render_template(
        "openapi.html",
        client_id=current_app.config["PKCE_CLIENT_ID"],
        scopes=current_app.config["PKCE_SCOPES"],
        redirect_url=redirect_url,
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
    backend_version = current_app.config.get("SMS_VERSION")
    servers = [
        {
            "url": url,
            "description": description,
        },
    ]
    token_endpoint = current_app.config.get("OIDC_TOKEN_ENDPOINT")
    # In case the frontend needs another url to access the token endpoint.
    # This are situations where a keycloak for example is part of the docker
    # network (so we can use the service name) - which the frontend can't do.
    if current_app.config.get("OIDC_TOKEN_ENDPOINT_FOR_FRONTEND"):
        token_endpoint = current_app.config.get("OIDC_TOKEN_ENDPOINT_FOR_FRONTEND")
    authorization_endpoint = current_app.config.get("OIDC_AUTHORIZATION_ENDPOINT")
    term_of_use_url = (
        current_app.config.get("SMS_FRONTEND_URL", "") + "/info/terms-of-use"
    )

    paths = {}
    components = {"responses": {}, "requestBodies": {}, "parameters": {}, "schemas": {}}
    # We externalized some of the openapi specs in order to make
    # their handling a bit easier.
    # We use python files - as they allow both setting the values explicitly
    # (as in json files), and it allows us to inspect the routes
    # and schemas that we expose.
    # Compared to plain json files it allows us to use comments within
    # the files too.
    # We load them from all the submodules in the openapi_parts folder.
    for submodule in pkgutil.iter_modules(openapi_parts.__path__):
        module_name = openapi_parts.__name__ + "." + submodule.name
        module_data = importlib.import_module(module_name)

        external_file_paths = getattr(module_data, "paths", {})
        for path in external_file_paths.keys():
            paths[path] = json.dumps(external_file_paths[path])
        external_file_components = getattr(module_data, "components", {})
        for component_type in components.keys():
            single_component_data = external_file_components.get(component_type, {})
            for key in single_component_data.keys():
                components[component_type][key] = json.dumps(single_component_data[key])

    result = render_template(
        "openapi.json",
        backend_version=backend_version,
        servers=servers,
        token_endpoint=token_endpoint,
        authorization_endpoint=authorization_endpoint,
        term_of_use_url=term_of_use_url,
        paths=paths,
        response_components=components["responses"],
        request_body_components=components["requestBodies"],
        parameter_components=components["parameters"],
        schema_components=components["schemas"],
    )
    return result, 200, {"Content-type": "application/json"}
