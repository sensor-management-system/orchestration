# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi specs for the generic platform actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.generic_actions_schema import GenericPlatformActionSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(GenericPlatformActionSchema)

paths = {
    "/generic-platform-actions": {
        "get": {
            "tags": ["Generic platform actions"],
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
                    "description": "List of generic platform actions",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Generic platform actions"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created generic platform action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/generic-platform-actions/{generic_platform_action_id}": {
        "get": {
            "tags": ["Generic platform actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/generic_platform_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a generic platform action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Generic platform actions"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_platform_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Generic platform action attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated generic platform action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Generic platform actions"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_platform_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "generic_platform_action_id": {
            "name": "generic_platform_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}
