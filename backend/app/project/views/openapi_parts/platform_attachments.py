# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi spec file for platform attachments."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.platform_attachment_schema import PlatformAttachmentSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(PlatformAttachmentSchema)

paths = {
    "/platform-attachments": {
        "get": {
            "tags": ["Platform attachments"],
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
                    "description": "List of platform attachments",
                    "content": {"application/vnd.api+json": schema_mapper.get_list()},
                }
            },
            "description": "Retrieve PlatformAttachment from platform_attachment",
            "operationId": "RetrieveacollectionofPlatformAttachmentobjects_0",
        },
        "post": {
            "tags": ["Platform attachments"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "description": "PlatformAttachment attributes",
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created platform attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
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
            },
            "operationId": "CreatePlatformAttachment_0",
        },
    },
    "/platform-attachments/{platform_attachment_id}": {
        "get": {
            "tags": ["Platform attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_attachment_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a platform attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve PlatformAttachment from platform_attachment",
            "operationId": "RetrievePlatformAttachmentinstance_0",
        },
        "patch": {
            "tags": ["Platform attachments"],
            "parameters": [{"$ref": "#/components/parameters/platform_attachment_id"}],
            "requestBody": {
                "description": "Payload to update a platform attachment",
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
            },
            "responses": {
                "200": {
                    "description": "Updated platform attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
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
                "409": {
                    "description": "Conflict on performing the operation",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {"$ref": "#/components/schemas/conflict"}
                        }
                    },
                },
            },
            "description": "Update PlatformAttachment attributes",
            "operationId": "UpdatePlatformAttachment_0",
        },
        "delete": {
            "tags": ["Platform attachments"],
            "parameters": [{"$ref": "#/components/parameters/platform_attachment_id"}],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
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
            "operationId": "DeletePlatformAttachmentfromplatformattachment_0",
        },
    },
    "/platform-attachments/{platform_attachment_id}/file/{filename}": {
        "get": {
            "tags": ["Platform attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_attachment_id"},
                {
                    "name": "filename",
                    "in": "path",
                    "required": True,
                    "description": (
                        "Filename of the file. Can be arbitrary, it "
                        "will always return the same file - no matter "
                        "how this parameter is set. "
                        "Backend needs this to allow linking of filenames for uploads."
                    ),
                    "schema": {"type": "string", "default": "file"},
                },
            ],
            "responses": {
                "200": {
                    "description": (
                        "Content of the file. Content-Type is the "
                        "same as the original upload."
                    ),
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
            "description": "Endpoint to get the content of the uploaded file.",
        }
    },
}

components = {
    "requestBodies": {},
    "schemas": {},
    "responses": {},
    "parameters": {
        "platform_attachment_id": {
            "name": "platform_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
