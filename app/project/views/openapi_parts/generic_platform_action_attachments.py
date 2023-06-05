# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the generic platform action attachments."""
paths = {
    "/generic-platform-action-attachments": {
        "get": {
            "tags": ["Generic platform action attachments"],
            "responses": {
                "200": {
                    "$ref": "#/components/responses/GenericPlatformActionAttachment_coll"
                }
            },
        },
        "post": {
            "tags": ["Generic platform action attachments"],
            "requestBody": {
                "$ref": "#/components/requestBodies/GenericPlatformActionAttachment_inst_post"
            },
            "responses": {
                "201": {
                    "$ref": "#/components/responses/GenericPlatformActionAttachment_inst"
                }
            },
        },
    },
    "/generic-platform-action-attachments/{generic_platform_action_attachment_id}": {
        "get": {
            "tags": ["Generic platform action attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {
                    "$ref": "#/components/parameters/generic_platform_action_attachment_id"
                },
            ],
            "responses": {
                "200": {
                    "$ref": "#/components/responses/GenericPlatformActionAttachment_coll"
                }
            },
        },
        "patch": {
            "tags": ["Generic platform action attachments"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/generic_platform_action_attachment_id"
                }
            ],
            "requestBody": {
                "$ref": "#/components/requestBodies/GenericPlatformActionAttachment_inst_patch"
            },
            "description": "",
            "responses": {
                "200": {
                    "$ref": "#/components/responses/GenericPlatformActionAttachment_coll"
                }
            },
        },
        "delete": {
            "tags": ["Generic platform action attachments"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/generic_platform_action_attachment_id"
                }
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "requestBodies": {
        "GenericPlatformActionAttachment_inst_post": {
            "description": "Generic platform action attachments instance.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string", "required": True},
                                    "attributes": {
                                        "type": "object",
                                        "required": True,
                                        "properties": {},
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": True,
                                        "properties": {
                                            "action": {
                                                "type": "object",
                                                "required": True,
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "required": True,
                                                        "properties": {
                                                            "id": {
                                                                "type": "string",
                                                                "required": True,
                                                            },
                                                            "type": {
                                                                "type": "string",
                                                                "required": True,
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                            "attachment": {
                                                "type": "object",
                                                "required": True,
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "required": True,
                                                        "properties": {
                                                            "id": {
                                                                "required": True,
                                                                "type": "string",
                                                            },
                                                            "type": {
                                                                "required": True,
                                                                "type": "string",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                        },
                                    },
                                },
                                "example": {
                                    "id": "123",
                                    "type": "generic_platform_action_attachment",
                                    "attributes": {},
                                    "relationships": {
                                        "action": {
                                            "type": "generic_platform_action",
                                            "id": "456",
                                        },
                                        "attachment": {
                                            "type": "platform_attachment",
                                            "id": "789",
                                        },
                                    },
                                },
                            }
                        }
                    }
                }
            },
        },
        "GenericPlatformActionAttachment_inst_patch": {
            "description": "Generic platform action attachments instance.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string", "required": True},
                                    "type": {"type": "string", "required": True},
                                    "attributes": {"type": "object", "properties": {}},
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "action": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "string",
                                                                "required": True,
                                                            },
                                                            "type": {
                                                                "type": "string",
                                                                "required": True,
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                            "attachment": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "required": True,
                                                                "type": "string",
                                                            },
                                                            "type": {
                                                                "required": True,
                                                                "type": "string",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                        },
                                    },
                                },
                                "example": {
                                    "id": "123",
                                    "type": "generic_platform_action_attachment",
                                    "attributes": {},
                                    "relationships": {
                                        "action": {
                                            "type": "generic_platform_action",
                                            "id": "456",
                                        },
                                        "attachment": {
                                            "type": "platform_attachment",
                                            "id": "789",
                                        },
                                    },
                                },
                            }
                        }
                    }
                }
            },
        },
    },
    "responses": {
        "GenericPlatformActionAttachment_coll": {
            "description": "List of generic platform action attachments.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "jsonapi": {
                                "type": "object",
                                "properties": {"version": {"type": "string"}},
                                "example": {"version": "1.0"},
                            },
                            "meta": {
                                "type": "object",
                                "properties": {"count": {"type": "number"}},
                                "example": {"count": 2},
                            },
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "type": {"type": "string"},
                                        "attributes": {"type": "object", "properties": {}},
                                        "relationships": {
                                            "type": "object",
                                            "properties": {
                                                "action": {
                                                    "type": "object",
                                                    "properties": {
                                                        "data": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {"type": "string"},
                                                                "type": {"type": "string"},
                                                            },
                                                        }
                                                    },
                                                },
                                                "attachment": {
                                                    "type": "object",
                                                    "properties": {
                                                        "data": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {"type": "string"},
                                                                "type": {"type": "string"},
                                                            },
                                                        }
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "example": [
                                    {
                                        "id": "123",
                                        "type": "generic_platform_action_attachment",
                                        "attributes": {},
                                        "relationships": {
                                            "action": {
                                                "type": "generic_platform_action",
                                                "id": "456",
                                            },
                                            "attachment": {
                                                "type": "platform_attachment",
                                                "id": "789",
                                            },
                                        },
                                    },
                                    {
                                        "id": "124",
                                        "type": "generic_platform_action_attachment",
                                        "attributes": {},
                                        "relationships": {
                                            "action": {
                                                "type": "generic_platform_action",
                                                "id": "457",
                                            },
                                            "attachment": {
                                                "type": "platform_attachment",
                                                "id": "780",
                                            },
                                        },
                                    },
                                ],
                            },
                        }
                    }
                }
            },
        },
        "GenericPlatformActionAttachment_inst": {
            "description": "Generic platform action attachments instance.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "jsonapi": {
                                "type": "object",
                                "properties": {"version": {"type": "string"}},
                                "example": {"version": "1.0"},
                            },
                            "data": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string"},
                                    "attributes": {"type": "object", "properties": {}},
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "action": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "attachment": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                        },
                                    },
                                },
                                "example": {
                                    "id": "123",
                                    "type": "generic_platform_action_attachment",
                                    "attributes": {},
                                    "relationships": {
                                        "action": {
                                            "type": "generic_platform_action",
                                            "id": "456",
                                        },
                                        "attachment": {
                                            "type": "platform_attachment",
                                            "id": "789",
                                        },
                                    },
                                },
                            },
                        }
                    }
                }
            },
        },
    },
    "parameters": {
        "generic_platform_action_attachment_id": {
            "name": "generic_platform_action_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
    "schemas": {
        "GenericPlatformActionAttachment_inst": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "default": "generic_platform_action_attachment",
                        },
                        "id": {"type": "string"},
                        "attributes": {"type": "object", "properties": {}},
                        "relationships": {
                            "type": "object",
                            "required": ["action", "attachment"],
                            "properties": {
                                "action": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "generic_platform_action",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                                "attachment": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "platform_attachment",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                            },
                        },
                    },
                }
            },
            "description": "Generic Platform Action Attachment Schema",
        }
    },
}
