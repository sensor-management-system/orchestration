# SPDX-FileCopyrightText: 2022 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""External openapi spec file for manufacturer models."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.manufacturer_model_schema import ManufacturerModelSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ManufacturerModelSchema)

paths = {
    "/manufacturer-models": {
        "get": {
            "tags": ["Manufacturer models"],
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
                    "description": "List of manufacturer models",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve the list of manufacturer models",
            "operationId": "RetrieveacollectionofManufacturerModelobjects_0",
        }
    },
    "/manufacturer-models/{manufacturer_model_id}": {
        "get": {
            "tags": ["Manufacturer models"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/manufacturer_model_id"},
            ],
            "responses": {
                "200": {
                    "description": "instance of a manufacturer model",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a manufacturer model instance",
            "operationId": "RetrieveManufacturerModelinstance_0",
        }
    },
}

components = {
    "parameters": {
        "manufacturer_model_id": {
            "name": "manufacturer_model_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
