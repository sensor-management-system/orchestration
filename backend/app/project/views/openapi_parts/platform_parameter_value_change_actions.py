# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi spec file for platform parameter value change actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.platform_parameter_value_change_action_schema import (
    PlatformParameterValueChangeActionSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(
    PlatformParameterValueChangeActionSchema
)

paths = {
    "/platform-parameter-value-change-actions": {
        "get": {
            "tags": ["Platform parameter value change actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of platform parameter value change actions",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve the list of platform parameter value change actions",
            "operationId": "RetriececollectionofPlatformParameterValueChangeActionobjects",
        },
        "post": {
            "tags": ["Platform parameter value change actions"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created platform parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreatePlatformParameterValuechangeAction",
        },
    },
    "/platform-parameter-value-change-actions/{platform_parameter_value_change_action_id}": {
        "get": {
            "tags": ["Platform parameter value change actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {
                    "$ref": "#/components/parameters/platform_parameter_value_change_action_id"
                },
            ],
            "responses": {
                "200": {
                    "description": "Instance of the platform parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single platform parameter value change action",
            "operationId": "RetrievePlatformParameterValueChangeActioninstance",
        },
        "patch": {
            "tags": ["Platform parameter value change actions"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/platform_parameter_value_change_action_id"
                },
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "PlatformParameterValueChangeAction attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated platform parameter value change action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update PlatformParameterValueChangeAction attributes",
            "operationId": "UpdatePlatformParameterValueChangeAction",
        },
        "delete": {
            "tags": ["Platform parameter value change actions"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/platform_parameter_value_change_action_id"
                }
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeletePlatformParameterValueChangeAction",
        },
    },
}

components = {
    "parameters": {
        "platform_parameter_value_change_action_id": {
            "name": "platform_parameter_value_change_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
