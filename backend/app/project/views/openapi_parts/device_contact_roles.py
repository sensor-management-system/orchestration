# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi part for the device contact roles."""

from ...api.schemas.json_schema import JSONSchema
from ...api.schemas.role import DeviceRoleSchema

schema = DeviceRoleSchema()

json_schema = JSONSchema().dump(schema)
paths = {
    "/device-contact-roles": {
        "get": {
            "tags": ["Device contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceContactRole_coll"}
            },
        },
        "post": {
            "tags": ["Device contact roles"],
            "requestBody": {
                "$ref": "#/components/requestBodies/DeviceContactRoles_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/DeviceContactRolel_inst"}
            },
        },
    },
    "/device-contact-roles/{device_contact_role_id}": {
        "get": {
            "tags": ["Device contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/device_contact_role_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/DeviceContactRole_inst"}
            },
        },
        "patch": {
            "tags": ["Device contact roles"],
            "parameters": [{"$ref": "#/components/parameters/device_contact_role_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/DeviceContactRoles"}
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/DeviceContactRole_inst"}
            },
        },
        "delete": {
            "tags": ["Device contact roles"],
            "parameters": [{"$ref": "#/components/parameters/device_contact_role_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}

components = {
    "responses": {
        "DeviceContactRole_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "id": "0",
                                        "type": "device_contact_role",
                                        "attributes": {
                                            "role_name": "PI",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "device": {
                                                "data": {"type": "device", "id": "123"}
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
                                        "type": "device_contact_role",
                                        "attributes": {
                                            "role_name": "Administrator",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "device": {
                                                "data": {"type": "device", "id": "1234"}
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
        "DeviceContactRole_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "device_contact_role",
                                    "attributes": {"role_name": "", "role_uri": ""},
                                    "relationships": {
                                        "device": {
                                            "data": {"type": "device", "id": "123"}
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
        "DeviceContactRoles_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "device_contact_role",
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
        "device_contact_role_id": {
            "name": "device_contact_role_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "DeviceContactRoles": {
            "properties": json_schema["properties"],
            "description": "Device Contact Roles Schema;",
        },
    },
}
