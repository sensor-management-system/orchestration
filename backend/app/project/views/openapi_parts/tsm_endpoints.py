# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Part of the openapi for datastream links."""

paths = {
    "/tsm-endpoints": {
        "get": {
            "tags": ["Tsm endpoints"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/TsmEndpoint_coll"}},
            "description": "Retrieve a collection of tsm endpoint objects",
            "operationId": "RetrieveacollectionofTsmEndpointObjects",
        },
    },
    "/tsm-endpoints/{tsm_endpoint_id}": {
        "get": {
            "tags": ["Tsm endpoints"],
            "parameters": [
                {"$ref": "#/components/parameters/tsm_endpoint_id"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/TsmEndpoint_inst"}},
            "description": "Retrieve a single Tsm endpoint object",
            "operationId": "RetrieveinstanceofTsmEndpointObject",
        },
    },
}
components = {
    "responses": {
        "TsmEndpoint_coll": {
            "description": "Data of a list of a TSM endpoints",
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
                                            "default": "tsm_endpoint",
                                        },
                                        "id": {
                                            "type": "string",
                                        },
                                        "attributes": {
                                            "type": "object",
                                            "properties": {
                                                "named": {"type": "string"},
                                                "url": {"type": "string"},
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
        "TsmEndpoint_inst": {
            "description": "Data of an instance of a TSM endpoint",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "tsm_endpoint",
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "url": {"type": "string"},
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
        "tsm_endpoint_id": {
            "name": "tsm_endpoint_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
