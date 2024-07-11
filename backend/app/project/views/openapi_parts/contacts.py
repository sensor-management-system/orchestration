# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Extenral openapi spec file for the contacts."""

from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.contact_schema import ContactSchema

schema_mapper = MarshmallowJsonApiToOpenApiMapper(ContactSchema)

paths = {
    "/contacts": {
        "get": {
            "tags": ["Contacts"],
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
                    "description": "List of contacts",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve Contact from contact",
            "operationId": "RetrieveacollectionofContactobjects_0",
        },
        "post": {
            "tags": ["Contacts"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created contact",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                }
            },
            "operationId": "CreateContact_0",
            "parameters": [],
        },
    },
    "/contacts/{contact_id}": {
        "get": {
            "tags": ["Contacts"],
            "parameters": [
                {"$ref": "#/components/parameters/contact_id"},
                {"$ref": "#/components/parameters/include"},
            ],
            "responses": {
                "200": {
                    "description": "Instance of a contact",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "description": "Retrieve Contact from contact",
            "operationId": "RetrieveContactinstance_0",
        },
        "patch": {
            "tags": ["Contacts"],
            "parameters": [{"$ref": "#/components/parameters/contact_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "Contact attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated contact",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "description": "Update Contact attributes",
            "operationId": "UpdateContact_0",
        },
        "delete": {
            "tags": ["Contacts"],
            "parameters": [{"$ref": "#/components/parameters/contact_id"}],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
            "operationId": "DeleteContactfromcontact_5",
        },
    },
}

components = {
    "parameters": {
        "contact_id": {
            "name": "contact_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
