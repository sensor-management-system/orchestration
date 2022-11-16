"""Openapi parts for configuration custom fields."""

paths = {
    "/configuration-customfields": {
        "get": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {
                    "name": "filter[key]",
                    "in": "query",
                    "required": False,
                    "description": "key attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[value]",
                    "in": "query",
                    "required": False,
                    "description": "value attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {
                    "name": "filter[configuration_id]",
                    "in": "query",
                    "required": False,
                    "description": "configuration_id attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/ConfigurationCustomField_coll"}
            },
            "description": "Retrieve a list of configuration custom fields",
            "operationId": "RetrieveacollectionofConfigurationCustomFieldobjects_0",
        },
        "post": {
            "tags": ["Configuration custom fields"],
            "requestBody": {
                "$ref": "#/components/requestBodies/ConfigurationCustomField_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/ConfigurationCustomField_coll"}
            },
            "operationId": "CreateConfigurationCustomField_0",
            "parameters": [],
        },
    },
    "/configuration-customfields/{configuration_custom_field_id}": {
        "get": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_custom_field_id"},
            ],
            "responses": {
                "200": {
                    "description": "Request fulfilled, document follows",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/ConfigurationCustomField"
                            }
                        }
                    },
                }
            },
            "description": "Retrieve a configuration custom field",
            "operationId": "RetrieveConfigurationCustomFieldinstance_0",
        },
        "patch": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_custom_field_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {
                            "$ref": "#/components/schemas/ConfigurationCustomField"
                        }
                    }
                },
                "description": "ConfigurationCustomField update payload",
                "required": True,
            },
            "responses": {
                "200": {"$ref": "#/components/responses/ConfigurationCustomField_coll"}
            },
            "description": "Update ConfigurationCustomField attributes",
            "operationId": "UpdateConfigurationCustomField_0",
        },
        "delete": {
            "tags": ["Configuration custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_custom_field_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteConfigurationCustomFieldfromcustomfield_0",
        },
    },
}

components = {
    "responses": {
        "ConfigurationCustomField_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "attributes": {"key": "", "value": ""},
                                    "type": "configuration_customfield",
                                    "id": "0",
                                    "relationships": {
                                        "configuration": {
                                            "data": None,
                                            "links": {
                                                "self": None,
                                            },
                                        }
                                    },
                                },
                                "type": "string",
                            }
                        },
                        "description": "ConfigurationCustomField get;",
                    }
                }
            },
            "description": "ConfigurationCustomField",
        },
    },
    "requestBodies": {
        "ConfigurationCustomField_inst": {
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
                                            "key": {"type": "string"},
                                            "value": {"type": "string"},
                                        },
                                    },
                                    "type": {
                                        "type": "string",
                                        "default": "configuration_customfield",
                                    },
                                },
                                "example": {
                                    "attributes": {"key": "", "value": ""},
                                    "relationships": {
                                        "configuration": {
                                            "data": {"type": "configuration", "id": "0"}
                                        }
                                    },
                                    "type": "configuration_customfield",
                                },
                            }
                        },
                        "description": "ConfigurationCustomField post;",
                    }
                }
            }
        },
    },
    "parameters": {
        "configuration_custom_field_id": {
            "name": "configuration_custom_field_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "ConfigurationCustomField": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "string"},
                                "value": {"type": "string"},
                            },
                        },
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "example": {
                        "attributes": {"key": "", "value": ""},
                        "relationships": {
                            "configuration": {
                                "data": {"type": "configuration", "id": "0"}
                            }
                        },
                        "type": "configuration_customfield",
                        "id": "0",
                    },
                }
            },
            "description": "ConfigurationCustomField Schema;",
        },
    },
}
