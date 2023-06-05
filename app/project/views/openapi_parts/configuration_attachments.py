# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for configuration attachments."""
paths = {
    "/configuration-attachments": {
        "get": {
            "tags": ["Configuration attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/label"},
                {"$ref": "#/components/parameters/url"},
                {"$ref": "#/components/parameters/configuration_id"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/ConfigurationAttachment_coll"}
            },
            "description": "Retrieve ConfigurationAttachment from configuration_attachment",
            "operationId": "RetrieveacollectionofConfigurationAttachmentobjects_0",
        },
        "post": {
            "tags": ["Configuration attachments"],
            "requestBody": {
                "$ref": "#/components/requestBodies/ConfigurationAttachment_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/ConfigurationAttachment_coll"}
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
                "200": {"$ref": "#/components/responses/ConfigurationAttachment_coll"}
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
                    "application/vnd.api+json": {
                        "schema": {
                            "$ref": "#/components/schemas/ConfigurationAttachment"
                        }
                    }
                },
                "description": "ConfigurationAttachment attributes",
                "required": True,
            },
            "responses": {
                "200": {"$ref": "#/components/responses/ConfigurationAttachment_coll"}
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
    "requestBodies": {
        "ConfigurationAttachment_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "attributes": {
                                        "type": "object",
                                        "required": ["label", "url"],
                                        "properties": {
                                            "label": {"type": "string"},
                                            "url": {"type": "string", "format": "url"},
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": ["configuration"],
                                        "properties": {
                                            "configuration": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": (
                                                                    "configuration_attachment"
                                                                ),
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            }
                                        },
                                    },
                                },
                            }
                        },
                        "description": "ConfigurationAttachment post;",
                    }
                }
            }
        },
    },
    "schemas": {
        "ConfigurationAttachment": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "url": {"type": "string", "format": "url"},
                                "is_upload": {"type": "boolean"},
                            },
                        },
                        "type": {"type": "string"},
                        "id": {"type": "string"},
                    },
                    "example": {
                        "attributes": {"label": "", "url": ""},
                        "type": "configuration_attachment",
                        "id": "0",
                    },
                }
            },
            "description": "ConfigurationAttachment Schema;",
        },
    },
    "responses": {
        "ConfigurationAttachment_coll": {
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
                                            "created_at": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "updated_at": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                        },
                                    },
                                    "type": {"type": "string"},
                                    "id": {"type": "string"},
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "configuration": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "created_by": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "updated_by": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                        },
                                    },
                                },
                                "example": {
                                    "attributes": {
                                        "label": "",
                                        "url": "",
                                        "is_upload": False,
                                        "created_at": "2023-03-14T12:00:00+00:00",
                                        "updated_at": "2023-03-14T13:00:00+00:00",
                                    },
                                    "relationships": {
                                        "configuration": {
                                            "data": {"type": "configuration", "id": "0"}
                                        },
                                        "created_by": {
                                            "data": {
                                                "type": "user",
                                                "id": "123",
                                            }
                                        },
                                        "updated_by": {
                                            "data": {
                                                "type": "user",
                                                "id": "124",
                                            }
                                        },
                                    },
                                    "type": "configuration_attachment",
                                    "id": "0",
                                },
                            }
                        },
                        "description": "ConfigurationAttachment get;",
                    }
                }
            },
            "description": "ConfigurationAttachment",
        },
    },
    "parameters": {
        "configuration_attachment_id": {
            "name": "configuration_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
