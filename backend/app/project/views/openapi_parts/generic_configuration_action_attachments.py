# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

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
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string"},
                                    "attributes": {
                                        "type": "object",
                                        "properties": {},
                                    },
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
                                                            },
                                                            "type": {
                                                                "type": "string",
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
                                                                "type": "string",
                                                            },
                                                            "type": {
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
                        },
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
                                                            "id": {
                                                                "type": "string",
                                                            },
                                                            "type": {
                                                                "type": "string",
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
                                                                "type": "string",
                                                            },
                                                            "type": {
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
                                        "attributes": {
                                            "type": "object",
                                            "properties": {},
                                        },
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
                                                                    "type": "string"
                                                                },
                                                                "type": {
                                                                    "type": "string"
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
                                                                    "type": "string"
                                                                },
                                                                "type": {
                                                                    "type": "string"
                                                                },
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
                        },
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
