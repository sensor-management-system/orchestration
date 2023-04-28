# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Part of the openapi for datastream links."""

paths = {
    "/datastream-links": {
        "get": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DatastreamLink_coll"}
            },
            "description": "Retrieve a collection of datastream link objects",
            "operationId": "RetrieveacollectionofDatastreamLinkObjects",
        },
        "post": {
            "tags": ["Datastream links"],
            "requestBody": {
                "$ref": "#/components/requestBodies/DatastreamLink_post",
            },
            "responses": {
                "201": {"$ref": "#/components/responses/DatastreamLink_inst"}
            },
            "operationId": "CreateDatastreamLink",
        },
    },
    "/datastream-links/{datastream_link_id}": {
        "get": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/datastream_link_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DatastreamLink_inst"}
            },
            "description": "Retrieve a single datastream link object",
            "operationId": "RetrieveinstanceofDatastreamLinkObject",
        },
        "patch": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/datastream_link_id"},
            ],
            "requestBody": {
                "$ref": "#/components/requestBodies/DatastreamLink_patch",
            },
            "responses": {
                "200": {"$ref": "#/components/responses/DatastreamLink_inst"}
            },
            "description": "Update a datastream link object",
            "operationId": "UpdateDatastreamLinkObject",
        },
        "delete": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/datastream_link_id"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "Delete a datastream link object",
        },
    },
}
components = {
    "requestBodies": {
        "DatastreamLink_post": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "datastream_link",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "tsm_endpoint": {"type": "string"},
                                            "datasource_id": {"type": "string"},
                                            "thing_id": {"type": "string"},
                                            "datastream_id": {"type": "string"},
                                            "datasource_name": {"type": "string"},
                                            "thing_name": {"type": "string"},
                                            "datastream_name": {"type": "string"},
                                            "begin_date": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "end_date": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "license_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "license_name": {
                                                "type": "string",
                                            },
                                            "aggregation_period": {"type": "number"},
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "device_mount_action": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_mount_action",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                            "device_property": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_property",
                                                            },
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
        "DatastreamLink_patch": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "datastream_link",
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "tsm_endpoint": {"type": "string"},
                                            "datasource_id": {"type": "string"},
                                            "thing_id": {"type": "string"},
                                            "datastream_id": {"type": "string"},
                                            "datasource_name": {"type": "string"},
                                            "thing_name": {"type": "string"},
                                            "datastream_name": {"type": "string"},
                                            "begin_date": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "end_date": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "license_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "license_name": {
                                                "type": "string",
                                            },
                                            "aggregation_period": {
                                                "type": "number",
                                            },
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "device_mount_action": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_mount_action",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                            "device_property": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_property",
                                                            },
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
    "responses": {
        "DatastreamLink_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "default": "datastream_link",
                                        },
                                        "id": {
                                            "type": "string",
                                        },
                                        "attributes": {
                                            "type": "object",
                                            "properties": {
                                                "tsm_endpoint": {"type": "string"},
                                                "datasource_id": {"type": "string"},
                                                "thing_id": {"type": "string"},
                                                "datastream_id": {"type": "string"},
                                                "datasource_name": {"type": "string"},
                                                "thing_name": {"type": "string"},
                                                "datastream_name": {"type": "string"},
                                                "begin_date": {
                                                    "type": "string",
                                                    "format": "date-time",
                                                },
                                                "end_date": {
                                                    "type": "string",
                                                    "format": "date-time",
                                                },
                                                "license_uri": {
                                                    "type": "string",
                                                    "format": "uri",
                                                },
                                                "license_name": {
                                                    "type": "string",
                                                },
                                                "aggregation_period": {
                                                    "type": "number",
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
                                        "relationships": {
                                            "type": "object",
                                            "properties": {
                                                "device_mount_action": {
                                                    "type": "object",
                                                    "properties": {
                                                        "data": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {
                                                                    "type": "string"
                                                                },
                                                                "type": {
                                                                    "type": "string",
                                                                },
                                                            },
                                                        }
                                                    },
                                                },
                                                "device_property": {
                                                    "type": "object",
                                                    "properties": {
                                                        "data": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {
                                                                    "type": "string"
                                                                },
                                                                "type": {
                                                                    "type": "string",
                                                                },
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
                                                                "id": {
                                                                    "type": "string"
                                                                },
                                                                "type": {
                                                                    "type": "string",
                                                                },
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
                                                                "id": {
                                                                    "type": "string"
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
                                },
                            }
                        }
                    }
                }
            }
        },
        "DatastreamLink_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "datastream_link",
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "tsm_endpoint": {"type": "string"},
                                            "datasource_id": {"type": "string"},
                                            "thing_id": {"type": "string"},
                                            "datastream_id": {"type": "string"},
                                            "datasource_name": {"type": "string"},
                                            "thing_name": {"type": "string"},
                                            "datastream_name": {"type": "string"},
                                            "begin_date": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "end_date": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "license_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "license_name": {
                                                "type": "string",
                                            },
                                            "aggregation_period": {
                                                "type": "number",
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
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "device_mount_action": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                            },
                                                        },
                                                    }
                                                },
                                            },
                                            "device_property": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                            },
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
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                            },
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
                                                            "id": {"type": "string"},
                                                            "type": {
                                                                "type": "string",
                                                                "default": "user",
                                                            },
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
        "datastream_link_id": {
            "name": "datastream_link_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
