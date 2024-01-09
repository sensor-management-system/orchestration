# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for configuration attachments."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.configuration_attachment_schema import ConfigurationAttachmentSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ConfigurationAttachmentSchema)

"""External openapi spec file for configuration attachments."""
paths = {
    "/configuration-attachments": {
        "get": {
            "tags": ["Configuration attachments"],
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
                    "description": "List of configuration attachments",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve ConfigurationAttachment from configuration_attachment",
            "operationId": "RetrieveacollectionofConfigurationAttachmentobjects_0",
        },
        "post": {
            "tags": ["Configuration attachments"],
            "requestBody": {
                "content": {"application/vnd.api+json": schema_mapper.post()},
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created configuration attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateConfigurationAttachment_0",
        },
    },
    "/configuration-attachments/{configuration_attachment_id}": {
        "get": {
            "tags": ["Configuration attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_attachment_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a configuration attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve ConfigurationAttachment from configuration_attachment",
            "operationId": "RetrieveConfigurationAttachmentinstance_0",
        },
        "patch": {
            "tags": ["Configuration attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_attachment_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "ConfigurationAttachment attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated configuration attachment",
                    "content": {"application/vnd.api+json": schema_mapper.get_one()},
                },
            },
            "description": "Update ConfigurationAttachment attributes",
            "operationId": "UpdateConfigurationAttachment_0",
        },
        "delete": {
            "tags": ["Configuration attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_attachment_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteConfigurationAttachmentfromconfigurationattachment_0",
        },
    },
    "/configuration-attachments/{configuration_attachment_id}/file/{filename}": {
        "get": {
            "tags": ["Configuration attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_attachment_id"},
                {
                    "name": "filename",
                    "in": "path",
                    "required": True,
                    "description": (
                        "Filename of the file. Can be arbitrary, "
                        "it will always return the same file - no "
                        "matter how this parameter is set. "
                        "Backend needs this to allow linking of filenames for uploads."
                    ),
                    "schema": {"type": "string", "default": "file"},
                },
            ],
            "responses": {
                "200": {
                    "description": (
                        "Content of the file. Content-Type "
                        "is the same as the original upload."
                    )
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": ("Endpoint to get the content of the uploaded file."),
        }
    },
}
components = {
    "parameters": {
        "configuration_attachment_id": {
            "name": "configuration_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
