# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi specs for the device mount actions."""
paths = {
    "/device-mount-actions": {
        "get": {
            "tags": ["Device mount actions"],
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceMountActions_coll"}
            },
        },
        "post": {
            "tags": ["Device mount actions"],
            "requestBody": {
                "$ref": "#/components/requestBodies/DeviceMountActions_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/DeviceMountActions_coll"}
            },
        },
    },
    "/device-mount-actions/{device_mount_action_id}": {
        "get": {
            "tags": ["Device mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_mount_action_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceMountActions_coll"}
            },
        },
        "patch": {
            "tags": ["Device mount actions"],
            "parameters": [{"$ref": "#/components/parameters/device_mount_action_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/DeviceMountActions"}
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/DeviceMountActions_coll"}
            },
        },
        "delete": {
            "tags": ["Device mount actions"],
            "parameters": [{"$ref": "#/components/parameters/device_mount_action_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "requestBodies": {
        "DeviceMountActions_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "device_mount_action",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "required": ["begin_date"],
                                        "properties": {
                                            "begin_description": {"type": "string"},
                                            "end_description": {"type": "string"},
                                            "begin_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                            "end_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                            "offset_x": {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            "offset_y": {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            "offset_z": {
                                                "type": "number",
                                                "format": "float",
                                            },
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "required": ["begin_contact"],
                                        "properties": {
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
                                            "device": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "parent_platform": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "platform",
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
        "DeviceMountActions_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "device_mount_action",
                                    "attributes": {
                                        "begin_description": "",
                                        "end_description": "",
                                        "begin_date": "",
                                        "end_date": "",
                                        "offset_x": "",
                                        "offset_y": "",
                                        "offset_z": "",
                                    },
                                    "relationships": {
                                        "configuration": {
                                            "data": {
                                                "type": "configuration",
                                                "id": "00",
                                            }
                                        },
                                        "device": {
                                            "data": {"type": "device", "id": "0"}
                                        },
                                        "parent_platform": {
                                            "data": {"type": "platform", "id": "00"}
                                        },
                                        "begin_contact": {
                                            "data": {"type": "contact", "id": "000"}
                                        },
                                        "end_contact": {
                                            "data": {"type": "contact", "id": "0000"}
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
    "schemas": {
        "DeviceMountActions": {
            "properties": {
                "data": {
                    "type": "object",
                    "required": ["type", "id"],
                    "properties": {
                        "type": {"type": "string", "default": "device_mount_action"},
                        "id": {"type": "string"},
                        "attributes": {
                            "type": "object",
                            "required": ["begin_date"],
                            "properties": {
                                "begin_description": {"type": "string"},
                                "end_description": {"type": "string"},
                                "begin_date": {"type": "string", "format": "datetime"},
                                "end_date": {"type": "string", "format": "datetime"},
                                "offset_x": {"type": "number", "format": "float"},
                                "offset_y": {"type": "number", "format": "float"},
                                "offset_z": {"type": "number", "format": "float"},
                            },
                        },
                        "relationships": {
                            "type": "object",
                            "required": ["begin_contact"],
                            "properties": {
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
                                "device": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "device",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                                "parent_platform": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "platform",
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
            "description": "Device Mount Actions Schema;",
        }
    },
}
