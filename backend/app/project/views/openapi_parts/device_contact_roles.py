# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi part for the device contact roles."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.role import DeviceRoleSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DeviceRoleSchema)

paths = {
    "/device-contact-roles": {
        "get": {
            "tags": ["Contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of device contact roles",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
        },
        "post": {
            "tags": ["Contact roles"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device contact role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/device-contact-roles/{device_contact_role_id}": {
        "get": {
            "tags": ["Contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_contact_role_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a device contct role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
        },
        "patch": {
            "tags": ["Contact roles"],
            "parameters": [{"$ref": "#/components/parameters/device_contact_role_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Device contact role attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the udpated device contact role",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
        },
        "delete": {
            "tags": ["Contact roles"],
            "parameters": [{"$ref": "#/components/parameters/device_contact_role_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}

components = {
    "parameters": {
        "device_contact_role_id": {
            "name": "device_contact_role_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
