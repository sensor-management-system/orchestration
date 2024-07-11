# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Externalized openapi spec for the platform mount actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.mount_actions_schema import PlatformMountActionSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(PlatformMountActionSchema)

paths = {
    "/platform-mount-actions": {
        "get": {
            "tags": ["Platform mount actions"],
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
                    "description": "List of platform mounts",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                },
            },
        },
        "post": {
            "tags": ["Platform mount actions"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created platform mount",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/platform-mount-actions/{platform_mount_action_id}": {
        "get": {
            "tags": ["Platform mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_mount_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a platform mount",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "patch": {
            "tags": ["Platform mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_mount_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "PlatformMountAction attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated platform mount",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
        "delete": {
            "tags": ["Platform mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_mount_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "platform_mount_action_id": {
            "name": "platform_mount_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
