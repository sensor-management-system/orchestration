"""External openapi spec file for device attachments."""

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
                "200": {"$ref": "#/components/responses/DeviceAttachment_coll"}
            },
            "description": "Retrieve DeviceAttachment from device_attachment",
            "operationId": "RetrieveacollectionofDeviceAttachmentobjects_0",
        },
        "post": {
            "tags": ["Device attachments"],
            "requestBody": {"$ref": "#/components/requestBodies/DeviceAttachment_inst"},
            "responses": {
                "201": {"$ref": "#/components/responses/DeviceAttachment_coll"}
            },
            "operationId": "CreateDeviceAttachment_0",
        },
    },
    "/device-attachments/{device_attachment_id}": {
        "get": {
            "tags": ["Device attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_attachments_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceAttachment_coll"}
            },
            "description": "Retrieve DeviceAttachment from device_attachment",
            "operationId": "RetrieveDeviceAttachmentinstance_0",
        },
        "patch": {
            "tags": ["Device attachments"],
            "parameters": [{"$ref": "#/components/parameters/device_attachments_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/DeviceAttachment"}
                    }
                },
                "description": "DeviceAttachment attributes",
                "required": True,
            },
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceAttachment_coll"}
            },
            "description": "Update DeviceAttachment attributes",
            "operationId": "UpdateDeviceAttachment_0",
        },
        "delete": {
            "tags": ["Device attachments"],
            "parameters": [{"$ref": "#/components/parameters/device_attachments_id"}],
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
                    "$ref": "#/components/errors/authentification_required",
                },
                "404": {
                    "$ref": "#/components/errors/not_found",
                },
            },
            "description": "Endpoint to get the content of the uploaded file.",
        }
    },
}

components = {
    "requestBodies": {
        "DeviceAttachment_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "label": {"type": "string"},
                                            "url": {"type": "string", "format": "url"},
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": ["device"],
                                        "properties": {
                                            "device": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_attachment",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                    },
                                    "type": {"type": "string"},
                                },
                            }
                        },
                        "description": "DeviceAttachment post",
                    }
                }
            }
        },
    },
    "schemas": {
        "DeviceAttachment": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "url": {"type": "string", "format": "url"},
                                "is_upload": {
                                    "type": "boolean",
                                },
                            },
                        },
                        "type": {"type": "string"},
                        "id": {"type": "string"},
                    },
                    "example": {
                        "attributes": {"label": "", "url": "", "is_upload": False},
                        "relationships": {
                            "device": {"data": {"type": "device", "id": "0"}}
                        },
                        "type": "device_attachment",
                        "id": "0",
                    },
                }
            },
            "description": "DeviceAttachment post;",
        },
    },
    "responses": {
        "DeviceAttachment_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "label": {"type": "string"},
                                            "url": {"type": "string", "format": "url"},
                                            "is_upload": {
                                                "type": "boolean",
                                            },
                                        },
                                    },
                                    "type": {"type": "string"},
                                    "id": {"type": "string"},
                                },
                                "example": {
                                    "attributes": {
                                        "label": "",
                                        "url": "",
                                        "is_upload": False,
                                    },
                                    "relationships": {
                                        "device": {
                                            "data": {"type": "device", "id": "0"}
                                        }
                                    },
                                    "type": "device_attachment",
                                    "id": "0",
                                },
                            }
                        },
                        "description": "DeviceAttachment get;",
                    }
                }
            },
            "description": "DeviceAttachment",
        },
    },
    "parameters": {
        "device_attachment_id": {
            "name": "device_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
