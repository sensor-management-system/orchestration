# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the permission groups."""
paths = {
    "/permission-groups": {
        "get": {
            "tags": ["Permission groups"],
            "parameters": [
                {
                    "name": "skip_cache",
                    "in": "query",
                    "required": False,
                    "default": False,
                    "schema": {"type": "boolean"},
                }
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/Permissiongroup_coll"}
            },
            "description": "Retrieve the list of permission groups.",
            "operationId": "get_permission_groups",
        }
    }
}
components = {
    "responses": {
        "Permissiongroup_coll": {
            "description": "List of permission groups.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "jsonapi": {
                                "type": "object",
                                "properties": {"version": {"type": "string"}},
                                "example": {"version": "1.0"},
                            },
                            "meta": {
                                "type": "object",
                                "properties": {"count": {"type": "number"}},
                                "example": {"count": 2},
                            },
                            "data": {
                                "type": "array",
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string"},
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "description": {"type": "string"},
                                        },
                                    },
                                },
                                "example": [
                                    {
                                        "id": "1",
                                        "type": "permission_group",
                                        "attributes": {
                                            "name": "Project A",
                                            "description": "A project one a nice place",
                                        },
                                    },
                                    {
                                        "id": "2",
                                        "type": "permission_group",
                                        "attributes": {
                                            "name": "Project B",
                                            "description": "Another project",
                                        },
                                    },
                                ],
                            },
                        }
                    }
                }
            },
        }
    },
    "schemas": {
        "GenericConfigurationActionAttachment_inst": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "default": "generic_configuration_action_attachment",
                        },
                        "id": {"type": "string"},
                        "attributes": {"type": "object", "properties": {}},
                        "relationships": {
                            "type": "object",
                            "required": ["action", "attachment"],
                            "properties": {
                                "action": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "generic_configuration_action",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                                "attachment": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "configuration_attachment",
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
            "description": "Generic Configuration Action Attachment Schema",
        }
    },
}
