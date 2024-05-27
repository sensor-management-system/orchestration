# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Part of the openapi for datastream links."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.tsm_endpoint_schema import TsmEndpointSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(TsmEndpointSchema)

paths = {
    "/tsm-endpoints": {
        "get": {
            "tags": ["Tsm endpoints"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {
                "200": {
                    "description": "List of TSM endpoints",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
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
            "responses": {
                "200": {
                    "description": "Instance of a TSM endpoint",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve a single Tsm endpoint object",
            "operationId": "RetrieveinstanceofTsmEndpointObject",
        },
    },
}
components = {
    "parameters": {
        "tsm_endpoint_id": {
            "name": "tsm_endpoint_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
