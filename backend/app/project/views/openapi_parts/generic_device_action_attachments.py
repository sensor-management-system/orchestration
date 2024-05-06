# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec fiel for the generic device action attachments."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.generic_action_attachment_schema import (
    GenericConfigurationActionAttachmentSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(
    GenericConfigurationActionAttachmentSchema
)

paths = {
    "/generic-device-action-attachments": {
        "get": {
            "tags": ["Generic device action attachments"],
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
                    "description": "List of generic device action attachments",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
        },
        "post": {
            "tags": ["Generic device action attachments"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created generic device action attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
        },
    },
    "/generic-device-action-attachments/{generic_device_action_attachment_id}": {
        "get": {
            "tags": ["Generic device action attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/generic_device_action_attachment_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a generic device action attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
        },
        "patch": {
            "tags": ["Generic device action attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_device_action_attachment_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Generic device action attachment attributes",
                "required": True,
            },
            "description": "",
            "responses": {
                "200": {
                    "description": "Payload of the updated generic device action attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
        },
        "delete": {
            "tags": ["Generic device action attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/generic_device_action_attachment_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "parameters": {
        "generic_device_action_attachment_id": {
            "name": "generic_device_action_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    }
}
