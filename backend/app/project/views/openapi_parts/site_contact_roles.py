# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Openapi part for the site contact roles."""

from ...api.schemas.json_schema import JSONSchema
from ...api.schemas.role import SiteRoleSchema

schema = SiteRoleSchema()

json_schema = JSONSchema().dump(schema)
paths = {
    "/site-contact-roles": {
        "get": {
            "tags": ["Site contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/SiteContactRole_coll"}
            },
        },
        "post": {
            "tags": ["Site contact roles"],
            "requestBody": {"$ref": "#/components/requestBodies/SiteContactRoles_inst"},
            "responses": {
                "201": {"$ref": "#/components/responses/SiteContactRolel_inst"}
            },
        },
    },
    "/site/{site_id}/site-contact-roles": {
        "get": {
            "tags": ["Site contact roles"],
            "responses": {
                "200": {"$ref": "#/components/responses/SiteContactRole_coll"}
            },
            "parameters": [
                {"$ref": "#/components/parameters/site_id"},
            ],
            "description": "Retrieve the contact roles for a specific site.",
        },
    },
    "/site-contact-roles/{site_contact_role_id}": {
        "get": {
            "tags": ["Site contact roles"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/site_contact_role_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/SiteContactRole_inst"}
            },
        },
        "patch": {
            "tags": ["Site contact roles"],
            "parameters": [{"$ref": "#/components/parameters/site_contact_role_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/SiteContactRoles"}
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/SiteContactRole_inst"}
            },
        },
        "delete": {
            "tags": ["Site contact roles"],
            "parameters": [{"$ref": "#/components/parameters/site_contact_role_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}

components = {
    "responses": {
        "SiteContactRole_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "id": "0",
                                        "type": "site_contact_role",
                                        "attributes": {
                                            "role_name": "PI",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "site": {
                                                "data": {"type": "site", "id": "123"}
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
                                        "type": "site_contact_role",
                                        "attributes": {
                                            "role_name": "Administrator",
                                            "role_uri": "",
                                        },
                                        "relationships": {
                                            "site": {
                                                "data": {"type": "site", "id": "1234"}
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
        "SiteContactRole_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "site_contact_role",
                                    "attributes": {"role_name": "", "role_uri": ""},
                                    "relationships": {
                                        "site": {"data": {"type": "site", "id": "123"}},
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
        "SiteContactRoles_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "site_contact_role",
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
                                            "site": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "site",
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
        "site_contact_role_id": {
            "name": "site_contact_role_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "SiteContactRoles": {
            "properties": json_schema["properties"],
            "description": "Site Contact Roles Schema;",
        },
    },
}
