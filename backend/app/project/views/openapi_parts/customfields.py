# SPDX-FileCopyrightText: 2022 - 2024
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi parts for device custom fields."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.customfield_schema import CustomFieldSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(CustomFieldSchema)

paths = {
    "/customfields": {
        "get": {
            "tags": ["Custom fields"],
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
                    "description": "List of customfields",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve CustomField from custom_field",
            "operationId": "RetrieveacollectionofCustomFieldobjects_0",
        },
        "post": {
            "tags": ["Custom fields"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created customfield",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateCustomField_0",
            "parameters": [],
        },
    },
    "/customfields/{custom_field_id}": {
        "get": {
            "tags": ["Custom fields"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/custom_field_id"},
            ],
            "responses": {
                "200": {
                    "description": "Request fulfilled, document follows",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Retrieve CustomField from custom_field",
            "operationId": "RetrieveCustomFieldinstance_0",
        },
        "patch": {
            "tags": ["Custom fields"],
            "parameters": [{"$ref": "#/components/parameters/custom_field_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "CustomField attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated customfield",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "description": "Update CustomField attributes",
            "operationId": "UpdateCustomField_0",
        },
        "delete": {
            "tags": ["Custom fields"],
            "parameters": [{"$ref": "#/components/parameters/custom_field_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteCustomFieldfromcustomfield_0",
        },
    },
}

components = {
    "parameters": {
        "custom_field_id": {
            "name": "custom_field_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
