# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the configuration endpoints."""

paths = {
    "/configurations": {
        "get": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/created_at"},
                {"$ref": "#/components/parameters/updated_at"},
                {"$ref": "#/components/parameters/start_date"},
                {"$ref": "#/components/parameters/end_date"},
                {"$ref": "#/components/parameters/label"},
                {"$ref": "#/components/parameters/status"},
                {"$ref": "#/components/parameters/created_by_id"},
                {"$ref": "#/components/parameters/updated_by_id"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
                {"$ref": "#/components/parameters/hide_archived"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/Configuration_coll"}},
            "description": "Retrieve Configuration from configuration",
            "operationId": "RetrieveacollectionofConfigurationobjects_0",
        },
        "post": {
            "tags": ["Configurations"],
            "description": "create a Configuration",
            "requestBody": {"$ref": "#/components/requestBodies/Configuration_inst"},
            "responses": {"201": {"$ref": "#/components/responses/Configuration_inst"}},
            "operationId": "CreateConfiguration_0",
        },
    },
    "/sites/{site_id}/configurations": {
        "get": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/created_at"},
                {"$ref": "#/components/parameters/updated_at"},
                {"$ref": "#/components/parameters/start_date"},
                {"$ref": "#/components/parameters/end_date"},
                {"$ref": "#/components/parameters/label"},
                {"$ref": "#/components/parameters/status"},
                {"$ref": "#/components/parameters/created_by_id"},
                {"$ref": "#/components/parameters/updated_by_id"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/site_id"},
                {"$ref": "#/components/parameters/filter"},
                {"$ref": "#/components/parameters/hide_archived"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/Configuration_coll"}},
            "description": "Retrieve the configurations for a specific site.",
            "operationId": "RetrieveacollectionofSite_0",
        },
    },
    "/configurations/{configuration_id}": {
        "get": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/Configuration_inst"}},
            "description": "Retrieve Configuration from configuration",
            "operationId": "RetrieveConfigurationinstance_0",
        },
        "patch": {
            "tags": ["Configurations"],
            "parameters": [{"$ref": "#/components/parameters/configuration_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/Configuration"}
                    }
                },
                "description": "Configuration attributes",
                "required": True,
            },
            "responses": {
                "200": {"$ref": "#/components/responses/Configuration_inst"},
            },
            "description": "Update Configuration attributes",
            "operationId": "UpdateConfiguration_0",
        },
        "delete": {
            "tags": ["Configurations"],
            "parameters": [{"$ref": "#/components/parameters/configuration_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteConfigurationfromconfiguration_0",
        },
    },
    "/configurations/{configuration_id}/archive": {
        "post": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "204": {"description": "Configuration was archived succesfully."},
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
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
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
            "description": "Archive a configuration.",
            "operationId": "ArchiveConfiguration",
        }
    },
    "/configurations/{configuration_id}/restore": {
        "post": {
            "tags": ["Configurations"],
            "parameters": [
                {"$ref": "#/components/parameters/configuration_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the configuration was succesful."},
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
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Restore an archived configuration.",
            "operationId": "RestoreConfiguration",
        }
    },
}
components = {
    "responses": {
        "Configuration_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "attributes": {
                                            "created_at": "2022-08-31T12:00:00",
                                            "updated_at": "2022-08-31T12:00:00",
                                            "start_date": "2022-08-31T12:00:00",
                                            "end_date": "2022-08-31T12:00:00",
                                            "label": "test cfg",
                                            "status": "draft",
                                            "cfg_permission_group": "1",
                                            "is_public": False,
                                            "is_internal": True,
                                            "archived": False,
                                            "description": "",
                                            "project": "",
                                            "persistent_identifier": "",
                                        },
                                        "type": "configuration",
                                        "id": "0",
                                        "relationships": {
                                            "site": {
                                                "data": {
                                                    "id": "123",
                                                    "type": "site",
                                                },
                                            },
                                            "configuration_static_location_actions": {
                                                "data": [],
                                                "links": {
                                                    "self": None,
                                                },
                                            },
                                            "configuration_dynamic_location_actions": {
                                                "data": [],
                                                "links": {
                                                    "self": None,
                                                },
                                            },
                                            "contact_role": {
                                                "data": [],
                                                "links": {
                                                    "self": None,
                                                },
                                            },
                                            "generic_configuration_actions": {
                                                "data": [],
                                                "links": {
                                                    "self": None,
                                                },
                                            },
                                            "platform_mount_actions": {
                                                "data": [],
                                                "links": {
                                                    "self": None,
                                                },
                                            },
                                            "device_mount_actions": {
                                                "data": [],
                                                "links": {
                                                    "self": None,
                                                },
                                            },
                                        },
                                    }
                                ],
                                "type": "string",
                            }
                        },
                        "description": "Configuration get;",
                    }
                }
            },
            "description": "Request fulfilled, document follows",
        },
        "Configuration_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "attributes": {
                                        "created_at": "2022-08-31T12:00:00",
                                        "updated_at": "2022-08-31T12:00:00",
                                        "start_date": "2022-08-31T12:00:00",
                                        "end_date": "2022-08-31T12:00:00",
                                        "label": "test cfg",
                                        "status": "draft",
                                        "cfg_permission_group": "1",
                                        "is_public": False,
                                        "is_internal": True,
                                        "archived": False,
                                        "description": "",
                                        "project": "",
                                        "persistent_identifier": "",
                                    },
                                    "type": "configuration",
                                    "id": "0",
                                    "relationships": {
                                        "site": {
                                            "data": {
                                                "id": "123",
                                                "type": "site",
                                            },
                                        },
                                        "configuration_static_location_actions": {
                                            "data": [],
                                            "links": {
                                                "self": None,
                                            },
                                        },
                                        "configuration_dynamic_location_actions": {
                                            "data": [],
                                            "links": {
                                                "self": None,
                                            },
                                        },
                                        "contact_role": {
                                            "data": [],
                                            "links": {
                                                "self": None,
                                            },
                                        },
                                        "generic_configuration_actions": {
                                            "data": [],
                                            "links": {
                                                "self": None,
                                            },
                                        },
                                        "platform_mount_actions": {
                                            "data": [],
                                            "links": {
                                                "self": None,
                                            },
                                        },
                                        "device_mount_actions": {
                                            "data": [],
                                            "links": {
                                                "self": None,
                                            },
                                        },
                                    },
                                },
                                "type": "string",
                            }
                        },
                        "description": "Configuration get;",
                    }
                }
            },
            "description": "Request fulfilled, document follows",
        },
    },
    "requestBodies": {
        "Configuration_inst": {
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
                                            "start_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                            "end_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                            "label": {"type": "string"},
                                            "status": {"type": "string"},
                                            "cfg_permission_group": {"type": "string"},
                                            "is_internal": {"type": "boolean"},
                                            "is_public": {"type": "boolean"},
                                            "description": {"type": "string"},
                                            "project": {"type": "string"},
                                            "persistent_identifier": {"type": "string"},
                                        },
                                    }
                                },
                                "example": {
                                    "attributes": {
                                        "start_date": "2022-08-31T12:00:00",
                                        "end_date": "2022-08-31T12:00:00",
                                        "label": "Test",
                                        "status": "draft",
                                        "cfg_permission_group": "0",
                                        "is_public": False,
                                        "is_internal": True,
                                        "archived": False,
                                        "description": "",
                                        "project": "",
                                        "persistent_identifier": "",
                                    },
                                    "type": "configuration",
                                    "relationships": {
                                        "site": {
                                            "data": {
                                                "id": "123",
                                                "type": "site",
                                            },
                                        },
                                    },
                                },
                            }
                        },
                        "description": "Configuration request body. For post & patch requests.",
                    }
                }
            }
        },
    },
    "parameters": {
        "configuration_id": {
            "name": "configuration_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "Configuration": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string", "default": "configuration"},
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "start_date": {"type": "string", "format": "datetime"},
                                "end_date": {"type": "string", "format": "datetime"},
                                "label": {"type": "string"},
                                "status": {"type": "string"},
                                "cfg_permission_group": {"type": "string"},
                                "is_internal": {"type": "boolean"},
                                "is_public": {"type": "boolean"},
                                "archived": {"type": "boolean"},
                                "description": {"type": "string"},
                                "project": {"type": "string"},
                                "persistent_identifier": {"type": "string"},
                            },
                        },
                        "relationships": {
                            "type": "object",
                            "properties": {
                                "site": {
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
                                                    "default": "site",
                                                },
                                            },
                                        },
                                    },
                                },
                                "created_by": {
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
                                                    "default": "user",
                                                },
                                            },
                                        },
                                    },
                                },
                                "updated_by": {
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
                                                    "default": "user",
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "example": {
                        "id": "0",
                        "attributes": {
                            "start_date": "2022-08-31T12:00:00",
                            "end_date": "2022-08-31T12:00:00",
                            "label": "",
                            "status": "draft",
                            "cfg_permission_group": "0",
                            "is_public": False,
                            "is_internal": True,
                            "archived": False,
                            "description": "",
                            "project": "",
                            "persistent_identifier": "",
                        },
                        "type": "configuration",
                    },
                }
            },
            "description": "Configuration Schema;",
        },
    },
}
