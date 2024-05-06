# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi spec for the dynamic location actions."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.configuration_dynamic_location_actions_schema import (
    ConfigurationDynamicLocationBeginActionSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(
    ConfigurationDynamicLocationBeginActionSchema
)

"""External openapi spec file for the dynamic location actions."""
paths = {
    "/dynamic-location-actions": {
        "get": {
            "tags": ["Dynamic location actions"],
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
                    "description": "List of dynamic locations",
                    "content": {
                        "application/vnd.api.json": schema_mapper.get_list(),
                    },
                }
            },
        },
        "post": {
            "tags": ["Dynamic location actions"],
            "requestBody": {
                "content": {
                    "application/vnd.api.json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created dynamic location action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
        },
    },
    "/dynamic-location-actions/{dynamic_location_action_id}": {
        "get": {
            "tags": ["Dynamic location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/dynamic_location_action_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a dynamic location action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
        },
        "patch": {
            "tags": ["Dynamic location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/dynamic_location_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Dynamic location action attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated dynamic location action",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
        },
        "delete": {
            "tags": ["Dynamic location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/dynamic_location_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "dynamic_location_action_id": {
            "name": "dynamic_location_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
