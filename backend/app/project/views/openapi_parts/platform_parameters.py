# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi spec file for platform parameters."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.platform_parameter_schema import PlatformParameterSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(PlatformParameterSchema)

paths = {
    "/platform-parameters": {
        "get": {
            "tags": ["Platform parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of platform parameters",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve the list of platform parameters",
            "operationId": "RetriececollectionofPlatformParameterobjects",
        },
        "post": {
            "tags": ["Platform parameters"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created platform parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreatePlatformParameter",
        },
    },
    "/platform-parameters/{platform_parameter_id}": {
        "get": {
            "tags": ["Platform parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_parameter_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a platform parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single platform parameter",
            "operationId": "RetrievePlatformParameterinstance",
        },
        "patch": {
            "tags": ["Platform parameters"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_parameter_id"},
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "PlatformParameter attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated platform parameter",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update PlatformParameter attributes",
            "operationId": "UpdatePlatformParameter",
        },
        "delete": {
            "tags": ["Platform parameters"],
            "parameters": [{"$ref": "#/components/parameters/platform_parameter_id"}],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeletePlatformParameter",
        },
    },
}

components = {
    "parameters": {
        "platform_parameter_id": {
            "name": "platform_parameter_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
