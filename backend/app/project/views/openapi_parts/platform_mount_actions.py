# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Externalized openapi spec for the platform mount actions."""
paths = {
    "/platform-mount-actions": {
        "get": {
            "tags": ["Platform mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformMountActions_coll"}
            },
        },
        "post": {
            "tags": ["Platform mount actions"],
            "requestBody": {
                "$ref": "#/components/requestBodies/PlatformMountActions_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/PlatformMountActions_coll"}
            },
        },
    },
    "/platform-mount-actions/{platform_mount_action_id}": {
        "get": {
            "tags": ["Platform mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_mount_action_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformMountActions_coll"}
            },
        },
        "patch": {
            "tags": ["Platform mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_mount_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/PlatformMountActions"}
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/PlatformMountActions_coll"}
            },
        },
        "delete": {
            "tags": ["Platform mount actions"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_mount_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
components = {
    "requestBodies": {
        "PlatformMountActions_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "platform_mount_action",
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
                                            "platform": {
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
        "PlatformMountActions_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "platform_mount_action",
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
                                        "platform": {
                                            "data": {"type": "platform", "id": "00"}
                                        },
                                        "parent_platform": {
                                            "data": {"type": "platform", "id": "00"}
                                        },
                                        "begin_contact": {
                                            "data": {"type": "contact", "id": "000"}
                                        },
                                        "end_contact": {
                                            "data": {"type": "contact", "id": "000"}
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
        "PlatformMountActions": {
            "properties": {
                "data": {
                    "type": "object",
                    "required": ["type", "id"],
                    "properties": {
                        "type": {"type": "string", "default": "platform_mount_action"},
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
                                "platform": {
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
            "description": "Platform Mount Actions Schema;",
        }
    },
}
