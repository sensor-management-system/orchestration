# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi specs for the device software update action attachments."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.software_update_action_attachment_schema import (
    DeviceSoftwareUpdateActionAttachmentSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(
    DeviceSoftwareUpdateActionAttachmentSchema
)

paths = {
    "/device-software-update-action-attachments": {
        "get": {
            "tags": ["Device software update action attachments"],
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
                    "description": "List of device software update action attachments",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Device software update action attachments"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device software update action attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/device-software-update-action-attachments/{device_software_update_action_attachment_id}": {
        "get": {
            "tags": ["Device software update action attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {
                    "$ref": "#/components/parameters/device_software_update_action_attachment_id"
                },
            ],
            "responses": {
                "200": {
                    "description": "Instance of a device software update action attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Device software update action attachments"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/device_software_update_action_attachment_id"
                }
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Device software update action attachment attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device software update action attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Device software update action attachments"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/device_software_update_action_attachment_id"
                }
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "device_software_update_action_attachment_id": {
            "name": "device_software_update_action_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    }
}
