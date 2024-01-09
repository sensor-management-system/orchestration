# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""External openapi spec file for the sites endpoints."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.site_schema import SiteSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(SiteSchema)

paths = {
    "/sites": {
        "get": {
            "tags": ["Sites"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
                {"$ref": "#/components/parameters/filter"},
                {"$ref": "#/components/parameters/hide_archived"},
            ],
            "responses": {
                "200": {
                    "description": "List of sites",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                },
            },
            "description": "Retrieve Site from site",
            "operationId": "RetrieveacollectionofSiteobjects_0",
        },
        "post": {
            "tags": ["Sites"],
            "description": "create a Site",
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created site",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateSite_0",
        },
    },
    "/sites/{site_id}": {
        "get": {
            "tags": ["Sites"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/site_id"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a site",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve Site from site",
            "operationId": "RetrieveSiteinstance_0",
        },
        "patch": {
            "tags": ["Sites"],
            "parameters": [{"$ref": "#/components/parameters/site_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Site attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated site",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update Site attributes",
            "operationId": "UpdateSite_0",
        },
        "delete": {
            "tags": ["Sites"],
            "parameters": [{"$ref": "#/components/parameters/site_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteSitefromsite_0",
        },
    },
    "/sites/{site_id}/sensorml": {
        "get": {
            "tags": ["Sites"],
            "parameters": [{"$ref": "#/components/parameters/site_id"}],
            "responses": {
                "200": {
                    "description": "SensorML response for the site",
                    "content": {"application/xml": {}},
                },
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
            },
            "description": "Retrieve Site sensorML",
            "operationId": "RetrieveSiteSensorML",
        },
    },
    "/sites/{site_id}/archive": {
        "post": {
            "tags": ["Sites"],
            "parameters": [
                {"$ref": "#/components/parameters/site_id"},
            ],
            "responses": {
                "204": {"description": "Site was archived succesfully."},
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
                "409": {
                    "description": "Conflict on performing the operation",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {"$ref": "#/components/schemas/conflict"}
                        }
                    },
                },
            },
            "description": "Archive a site.",
            "operationId": "ArchiveSite",
        }
    },
    "/sites/{site_id}/restore": {
        "post": {
            "tags": ["Sites"],
            "parameters": [
                {"$ref": "#/components/parameters/site_id"},
            ],
            "responses": {
                "204": {"description": "Restoring of the site was succesful."},
                "401": {
                    "description": "Authentification required.",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {
                                "$ref": "#/components/schemas/authentification_required"
                            }
                        }
                    },
                },
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Restore an archived site.",
            "operationId": "RestoreSite",
        }
    },
}
components = {
    "parameters": {
        "site_id": {
            "name": "site_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
