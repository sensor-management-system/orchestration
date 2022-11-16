"""Openapi parts for device custom fields."""

paths = {
    "/customfields": {
        "get": {
            "tags": ["Custom fields"],
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
                    "name": "filter[device_id]",
                    "in": "query",
                    "required": False,
                    "description": "device_id attribute filter.",
                    "schema": {"type": "string", "format": "string", "default": ""},
                },
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/CustomField_coll"}},
            "description": "Retrieve CustomField from custom_field",
            "operationId": "RetrieveacollectionofCustomFieldobjects_0",
        },
        "post": {
            "tags": ["Custom fields"],
            "requestBody": {"$ref": "#/components/requestBodies/CustomField_inst"},
            "responses": {"201": {"$ref": "#/components/responses/CustomField_coll"}},
            "operationId": "CreateCustomField_0",
            "parameters": [],
        },
    },
    "/customfields/{custom_field_id}": {
        "get": {
            "tags": ["Custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/custom_field_id"},
            ],
            "responses": {
                "200": {
                    "description": "Request fulfilled, document follows",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {"$ref": "#/components/schemas/CustomField"}
                        }
                    },
                }
            },
            "description": "Retrieve CustomField from custom_field",
            "operationId": "RetrieveCustomFieldinstance_0",
        },
        "patch": {
            "tags": ["Custom fields"],
            "parameters": [{"$ref": "#/components/parameters/custom_field_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/CustomField"}
                    }
                },
                "description": "CustomField attributes",
                "required": True,
            },
            "responses": {"200": {"$ref": "#/components/responses/CustomField_coll"}},
            "description": "Update CustomField attributes",
            "operationId": "UpdateCustomField_0",
        },
        "delete": {
            "tags": ["Custom fields"],
            "parameters": [{"$ref": "#/components/parameters/custom_field_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteCustomFieldfromcustomfield_0",
        },
    },
}

components = {
    "responses": {
        "CustomField_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "attributes": {"key": "", "value": ""},
                                    "type": "customfield",
                                    "id": "0",
                                    "relationships": {
                                        "device": {
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
                        "description": "CustomField get;",
                    }
                }
            },
            "description": "CustomField",
        },
    },
    "requestBodies": {
        "CustomField_inst": {
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
                                        "default": "customfield",
                                    },
                                },
                                "example": {
                                    "attributes": {"key": "", "value": ""},
                                    "relationships": {
                                        "device": {
                                            "data": {"type": "device", "id": "0"}
                                        }
                                    },
                                    "type": "customfield",
                                },
                            }
                        },
                        "description": "CustomField post;",
                    }
                }
            }
        },
    },
    "parameters": {
        "custom_field_id": {
            "name": "custom_field_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "CustomField": {
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
                            "device": {"data": {"type": "device", "id": "0"}}
                        },
                        "type": "customfield",
                        "id": "0",
                    },
                }
            },
            "description": "CustomField Schema;",
        },
    },
}
