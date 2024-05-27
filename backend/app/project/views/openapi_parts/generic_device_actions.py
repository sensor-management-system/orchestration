# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi specs for the generic device actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.generic_actions_schema import GenericDeviceActionSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(GenericDeviceActionSchema)

paths = {
    "/generic-device-actions": {
        "get": {
            "tags": ["Generic device actions"],
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
                    "description": "List of generic device actions",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Generic device actions"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created generic device action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/generic-device-actions/{generic_device_action_id}": {
        "get": {
            "tags": ["Generic device actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/generic_device_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a generic device action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Generic device actions"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_device_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Generic device action attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated generic device action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Generic device actions"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_device_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "generic_device_action_id": {
            "name": "generic_device_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}
