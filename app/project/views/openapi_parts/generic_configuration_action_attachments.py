"""External openapi spec file for generic configuration action attachments."""
paths = {
    "/generic-configuration-action-attachments": {
        "get": {
            "tags": ["Generic configuration action attachments"],
            "responses": {
                "200": {
                    "$ref": "#/components/responses/GenericConfigurationActionAttachment_coll"
                }
            },
        },
        "post": {
            "tags": ["Generic configuration action attachments"],
            "requestBody": {
                "$ref": "#/components/requestBodies/GenericConfigurationActionAttachment_inst_post"
            },
            "responses": {
                "201": {
                    "$ref": "#/components/responses/GenericConfigurationActionAttachment_inst"
                }
            },
        },
    },
    "/generic-configuration-action-attachments/{generic_configuration_action_attachment_id}": {
        "get": {
            "tags": ["Generic configuration action attachments"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {
                    "$ref": "#/components/parameters/generic_configuration_action_attachment_id"
                },
            ],
            "responses": {
                "200": {
                    "$ref": "#/components/responses/GenericConfigurationActionAttachment_coll"
                }
            },
        },
        "patch": {
            "tags": ["Generic configuration action attachments"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/generic_configuration_action_attachment_id"
                }
            ],
            "requestBody": {
                "$ref": "#/components/requestBodies/GenericConfigurationActionAttachment_inst_patch"
            },
            "description": "",
            "required": True,
            "responses": {
                "200": {
                    "$ref": "#/components/responses/GenericConfigurationActionAttachment_coll"
                }
            },
        },
        "delete": {
            "tags": ["Generic configuration action attachments"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/generic_configuration_action_attachment_id"
                }
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "requestBodies": {
        "GenericConfigurationActionAttachment_inst_post": {
            "description": "Generic configuration action attachments instance.",
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
                                    "type": "generic_configuration_action_attachment",
                                    "attributes": {},
                                    "relationships": {
                                        "action": {
                                            "type": "generic_configuration_action",
                                            "id": "456",
                                        },
                                        "attachment": {
                                            "type": "configuration_attachment",
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
        "GenericConfigurationActionAttachment_inst_patch": {
            "description": "Generic configuration action attachments instance.",
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
                                    "type": "generic_configuration_action_attachment",
                                    "attributes": {},
                                    "relationships": {
                                        "action": {
                                            "type": "generic_configuration_action",
                                            "id": "456",
                                        },
                                        "attachment": {
                                            "type": "configuration_attachment",
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
        "GenericConfigurationActionAttachment_coll": {
            "description": "List of generic configuration action attachments.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
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
                                "example": [
                                    {
                                        "id": "123",
                                        "type": "generic_configuration_action_attachment",
                                        "attributes": {},
                                        "relationships": {
                                            "action": {
                                                "type": "generic_configuration_action",
                                                "id": "456",
                                            },
                                            "attachment": {
                                                "type": "configuration_attachment",
                                                "id": "789",
                                            },
                                        },
                                    },
                                    {
                                        "id": "124",
                                        "type": "generic_configuration_action_attachment",
                                        "attributes": {},
                                        "relationships": {
                                            "action": {
                                                "type": "generic_configuration_action",
                                                "id": "457",
                                            },
                                            "attachment": {
                                                "type": "configuration_attachment",
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
        "GenericConfigurationActionAttachment_inst": {
            "description": "Generic configuration action attachments instance.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
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
                                    "type": "generic_configuration_action_attachment",
                                    "attributes": {},
                                    "relationships": {
                                        "action": {
                                            "type": "generic_configuration_action",
                                            "id": "456",
                                        },
                                        "attachment": {
                                            "type": "configuration_attachment",
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
        "generic_configuration_action_attachment_id": {
            "name": "generic_configuration_action_attachment_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
