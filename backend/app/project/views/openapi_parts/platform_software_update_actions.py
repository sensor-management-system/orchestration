# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi specs for the platform software update actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.software_update_action_schema import (
    PlatformSoftwareUpdateActionSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(PlatformSoftwareUpdateActionSchema)

paths = {
    "/platform-software-update-actions": {
        "get": {
            "tags": ["Platform software update actions"],
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
                    "description": "List of platform software update actions",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Platform software update actions"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created platform software update action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/platform-software-update-actions/{platform_software_update_action_id}": {
        "get": {
            "tags": ["Platform software update actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_software_update_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a platform software update action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Platform software update actions"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_software_update_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Platform software update action attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated platform software update action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Platform software update actions"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_software_update_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "platform_software_update_action_id": {
            "name": "platform_software_update_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}