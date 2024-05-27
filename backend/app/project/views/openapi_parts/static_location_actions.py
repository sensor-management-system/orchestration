# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Externalized openapi spec for the static location actions."""
from ... import api
from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.resources import (
    ConfigurationStaticLocationBeginActionDetail,
    ConfigurationStaticLocationBeginActionList,
)
from ...api.schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationBeginActionSchema,
)


class ApiInspector:
    """
    Helper class to inspect the api object.

    Helps to extract resources & their urls.
    """

    def __init__(self, api):
        """Init the object."""
        self.api = api

    def find_registered_resource(self, registered_resource):
        """Find a registered resource with its urls or None."""
        for resource in api.resources:
            if resource["resource"] == registered_resource:
                return resource
        return None


inspector = ApiInspector(api)
# Here we are going to start to generate the spec from the
# resources that we already have.
list_resource = inspector.find_registered_resource(
    ConfigurationStaticLocationBeginActionList
)
# We can have multiple ones that could have more path parameters:
# /static-location/actions and
# /configurations/<int:configuration_id>/static-location-actions
#
# First one is the more general one without further parameters.
url_list_endpoint = list_resource["urls"][0]

detail_resource = inspector.find_registered_resource(
    ConfigurationStaticLocationBeginActionDetail
)

# The id parameter for the detail view doesn't follow the conventions
# that we use in the openapi spec - so we replace it.
url_detail_endpoint = detail_resource["urls"][0].replace(
    "<int:id>", "{static_location_action_id}"
)

# Other things that we could read from the resources are possible status
# codes, descriptions, ...

schema_mapper = MarshmallowJsonApiToOpenApiMapper(
    ConfigurationStaticLocationBeginActionSchema
)

paths = {
    url_list_endpoint: {
        "get": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {
                    "description": "List of static locations",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Get the list of static location actions.",
        },
        "post": {
            "tags": ["Static location actions"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created static location",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
        },
    },
    url_detail_endpoint: {
        "get": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/static_location_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a static location",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
        },
        "patch": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/static_location_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Static location attributes",
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the updated static location",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/static_location_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "static_location_action_id": {
            "name": "static_location_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
