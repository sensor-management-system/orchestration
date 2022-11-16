"""Openapi part for the configuration contact roles."""

from ...api.schemas.json_schema import JSONSchema
from ...api.schemas.role import ConfigurationRoleSchema

schema = ConfigurationRoleSchema()
json_schema = JSONSchema().dump(schema)

paths = {
    "/configuration-contact-roles": {
        "get": {
            "tags": ["Configuration contact roles"],
            "responses": {
                "200": {"$ref": "#/components/responses/ConfigurationContactRole_coll"}
            },
        },
        "post": {
            "tags": ["Configuration contact roles"],
            "requestBody": {
                "$ref": "#/components/requestBodies/ConfigurationContactRoles_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/ConfigurationContactRolel_inst"}
            },
        },
    },
    "/configuration-contact-roles/{configuration_contact_role_id}": {
        "get": {
            "tags": ["Configuration contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_contact_role_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/ConfigurationContactRole_inst"}
            },
        },
        "patch": {
            "tags": ["Configuration contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_contact_role_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {
                            "$ref": "#/components/schemas/ConfigurationContactRoles"
                        }
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/ConfigurationContactRole_inst"}
            },
        },
        "delete": {
            "tags": ["Configuration contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_contact_role_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}

components = {
    "responses": {
        "ConfigurationContactRole_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "id": "0",
                                        "type": "configuration_contact_role",
                                        "attributes": {
                                            "role_name": "PI",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "configuration": {
                                                "data": {
                                                    "type": "configuration",
                                                    "id": "123",
                                                }
                                            },
                                            "contact": {
                                                "data": {
                                                    "type": "contact",
                                                    "id": "000",
                                                },
                                            },
                                        },
                                    },
                                    {
                                        "id": "1",
                                        "type": "configuration_contact_role",
                                        "attributes": {
                                            "role_name": "Administrator",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "configuration": {
                                                "data": {
                                                    "type": "configuration",
                                                    "id": "1234",
                                                }
                                            },
                                            "contact": {
                                                "data": {
                                                    "type": "contact",
                                                    "id": "1",
                                                },
                                            },
                                        },
                                    },
                                ]
                            }
                        }
                    }
                }
            },
            "description": "",
        },
        "ConfigurationContactRole_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "configuration_contact_role",
                                    "attributes": {"role_name": "", "role_uri": ""},
                                    "relationships": {
                                        "configuration": {
                                            "data": {
                                                "type": "configuration",
                                                "id": "123",
                                            }
                                        },
                                        "contact": {
                                            "data": {"type": "contact", "id": "000"},
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "description": "",
        },
    },
    "requestBodies": {
        "ConfigurationContactRoles_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "configuration_contact_role",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "role_name": {"type": "string"},
                                            "role_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": ["contact"],
                                        "properties": {
                                            "contact": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "contact",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "configuration": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "configuration",
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
                        }
                    }
                }
            }
        },
    },
    "parameters": {
        "configuration_contact_role_id": {
            "name": "configuration_contact_role_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "ConfigurationContactRoles": {
            "properties": json_schema["properties"],
            "description": "Configuration Contact Roles Schema;",
        },
    },
}
