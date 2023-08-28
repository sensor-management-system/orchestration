# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi part for the platform contact roles."""

from ...api.schemas.json_schema import JSONSchema
from ...api.schemas.role import PlatformRoleSchema

schema = PlatformRoleSchema()

json_schema = JSONSchema().dump(schema)

paths = {
    "/platform-contact-roles": {
        "get": {
            "tags": ["Platform contact roles"],
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformContactRole_coll"}
            },
        },
        "post": {
            "tags": ["Platform contact roles"],
            "requestBody": {
                "$ref": "#/components/requestBodies/PlatformContactRoles_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/PlatformContactRolel_inst"}
            },
        },
    },
    "/platform-contact-roles/{platform_contact_role_id}": {
        "get": {
            "tags": ["Platform contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/platform_contact_role_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/PlatformContactRole_inst"}
            },
        },
        "patch": {
            "tags": ["Platform contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_contact_role_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/PlatformContactRoles"}
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/PlatformContactRole_inst"}
            },
        },
        "delete": {
            "tags": ["Platform contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/platform_contact_role_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}

components = {
    "responses": {
        "PlatformContactRole_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "id": "0",
                                        "type": "platform_contact_role",
                                        "attributes": {
                                            "role_name": "PI",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "platform": {
                                                "data": {
                                                    "type": "platform",
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
                                        "type": "platform_contact_role",
                                        "attributes": {
                                            "role_name": "Administrator",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "platform": {
                                                "data": {
                                                    "type": "platform",
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
        "PlatformContactRole_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "platform_contact_role",
                                    "attributes": {"role_name": "", "role_uri": ""},
                                    "relationships": {
                                        "platform": {
                                            "data": {"type": "platform", "id": "123"}
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
        "PlatformContactRoles_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "platform_contact_role",
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
        "platform_contact_role_id": {
            "name": "platform_contact_role_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "PlatformContactRoles": {
            "properties": json_schema["properties"],
            "description": "Platform Contact Roles Schema;",
        },
    },
}
