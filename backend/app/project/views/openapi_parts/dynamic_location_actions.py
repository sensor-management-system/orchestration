# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the dynamic location actions."""
paths = {
    "/dynamic-location-actions": {
        "get": {
            "tags": ["Dynamic location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DynamicLocationAction_coll"}
            },
        },
        "post": {
            "tags": ["Dynamic location actions"],
            "requestBody": {
                "$ref": "#/components/requestBodies/DynamicLocationAction_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/DynamicLocationAction_coll"}
            },
        },
    },
    "/dynamic-location-actions/{dynamic_location_action_id}": {
        "get": {
            "tags": ["Dynamic location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/dynamic_location_action_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DynamicLocationAction_coll"}
            },
        },
        "patch": {
            "tags": ["Dynamic location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/dynamic_location_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/DynamicLocationAction"}
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/DynamicLocationAction_coll"}
            },
        },
        "delete": {
            "tags": ["Dynamic location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/dynamic_location_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "requestBodies": {
        "DynamicLocationAction_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "configuration_dynamic_location_action",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "begin_description": {"type": "string"},
                                            "end_description": {"type": "string"},
                                            "label": {"type": "string"},
                                            "epsg_code": {
                                                "type": "string",
                                                "default": "4326",
                                            },
                                            "elevation_datum_name": {
                                                "type": "string",
                                                "default": "MSL",
                                            },
                                            "elevation_datum_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "begin_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                            "end_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": ["contact"],
                                        "properties": {
                                            "begin_contact": {
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
                                            "end_contact": {
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
                                            "x_property": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_property",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "y_property": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_property",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "z_property": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_property",
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
        }
    },
    "responses": {
        "DynamicLocationAction_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "configuration_dynamic_location_action",
                                    "attributes": {
                                        "begin_description": "",
                                        "end_description": "",
                                        "label": "",
                                        "begin_date": "",
                                        "end_date": "",
                                        "epsg_code": "",
                                        "elevation_datum_name": "",
                                        "elevation_datum_uri": "",
                                        "action_type_uri": "",
                                    },
                                    "relationships": {
                                        "configuration": {
                                            "data": {
                                                "type": "configuration",
                                                "id": "00",
                                            }
                                        },
                                        "begin_contact": {
                                            "data": {"type": "contact", "id": "000"}
                                        },
                                        "end_contact": {
                                            "data": {"type": "contact", "id": "000"}
                                        },
                                        "x_property": {"type": "contact", "id": "000"},
                                        "y_property": {
                                            "type": "device_property",
                                            "id": "000",
                                        },
                                        "z_property": {
                                            "type": "device_property",
                                            "id": "000",
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "description": "",
        }
    },
    "parameters": {
        "dynamic_location_action_id": {
            "name": "dynamic_location_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
    "schemas": {
        "DynamicLocationAction": {
            "properties": {
                "data": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "type": {
                            "type": "string",
                            "default": "configuration_dynamic_location_begin_action",
                        },
                        "id": {"type": "string"},
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "begin_description": {"type": "string"},
                                "end_description": {"type": "string"},
                                "label": {"type": "string"},
                                "epsg_code": {"type": "string", "default": "4326"},
                                "elevation_datum_name": {
                                    "type": "string",
                                    "default": "MSL",
                                },
                                "elevation_datum_uri": {
                                    "type": "string",
                                    "format": "uri",
                                },
                                "begin_date": {"type": "string", "format": "datetime"},
                                "end_date": {"type": "string", "format": "datetime"},
                            },
                        },
                        "relationships": {
                            "type": "object",
                            "required": ["begin_contact"],
                            "properties": {
                                "begin_contact": {
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
                                "end_contact": {
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
                                "x_property": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "device_property",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                                "y_property": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "device_property",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                                "z_property": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "device_property",
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
            "description": "Dynamic Location Action Schema;",
        }
    },
}
