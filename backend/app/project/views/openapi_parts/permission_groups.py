# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

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
                    "schema": {"type": "boolean", "default": False},
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
                        "type": "object",
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
                                "items": {
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
                        },
                    }
                }
            },
        }
    },
}
