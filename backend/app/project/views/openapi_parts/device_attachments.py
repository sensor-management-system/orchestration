# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for device attachments."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.device_attachment_schema import DeviceAttachmentSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(DeviceAttachmentSchema)

paths = {
    "/device-attachments": {
        "get": {
            "tags": ["Device attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {
                    "name": "filter[label]",
                    "in": "query",
                    "required": False,
                    "description": "label attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {"$ref": "#/components/parameters/url"},
                {
                    "name": "filter[device_id]",
                    "in": "query",
                    "required": False,
                    "description": "device_id attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {
                    "description": "List of device attachments",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve DeviceAttachment from device_attachment",
            "operationId": "RetrieveacollectionofDeviceAttachmentobjects_0",
        },
        "post": {
            "tags": ["Device attachments"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created device attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateDeviceAttachment_0",
        },
    },
    "/device-attachments/{device_attachment_id}": {
        "get": {
            "tags": ["Device attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_attachment_id"},
            ],
            "responses": {
                "200": {
                    "description": "instance of a device attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve DeviceAttachment from device_attachment",
            "operationId": "RetrieveDeviceAttachmentinstance_0",
        },
        "patch": {
            "tags": ["Device attachments"],
            "parameters": [{"$ref": "#/components/parameters/device_attachment_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "DeviceAttachment attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated device attachment",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "description": "Update DeviceAttachment attributes",
            "operationId": "UpdateDeviceAttachment_0",
        },
        "delete": {
            "tags": ["Device attachments"],
            "parameters": [{"$ref": "#/components/parameters/device_attachment_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteDeviceAttachmentfromdeviceattachment_0",
        },
    },
    "/device-attachments/{device_attachment_id}/file/{filename}": {
        "get": {
            "tags": ["Device attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/device_attachment_id"},
                {
                    "name": "filename",
                    "in": "path",
                    "required": True,
                    "description": (
                        "Filename of the file. Can be arbitrary, it "
                        "will always return the same file - no matter"
                        " how this parameter is set. "
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
    "parameters": {
        "device_attachment_id": {
            "name": "device_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
