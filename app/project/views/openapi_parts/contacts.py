# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Extenrla openapi spec file for the contacts."""

paths = {
    "/contacts": {
        "get": {
            "tags": ["Contacts"],
            "parameters": [
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/website"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/given_name"},
                {"$ref": "#/components/parameters/family_name"},
                {"$ref": "#/components/parameters/email"},
                {
                    "name": "filter[organization]",
                    "in": "query",
                    "required": False,
                    "description": "Filter the contacts by organization name.",
                    "schema": {
                        "type": "string",
                        "format": "string",
                        "default": "",
                    }
                },
                {
                    "name": "filter[orcid]",
                    "in": "query",
                    "required": False,
                    "description": "Filter the contacts by orcid.",
                    "schema": {
                        "type": "string",
                        "format": "string",
                        "default": "",
                    }
                },
                {"$ref": "#/components/parameters/filter"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/Contact_coll1"}},
            "description": "Retrieve Contact from contact",
            "operationId": "RetrieveacollectionofContactobjects_0",
        },
        "post": {
            "tags": ["Contacts"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/Contact"}
                    }
                },
                "description": "Contact attributes",
                "required": True,
            },
            "responses": {"201": {"$ref": "#/components/responses/Contact_coll1"}},
            "operationId": "CreateContact_0",
            "parameters": [],
        },
    },
    "/contacts/{contact_id}": {
        "get": {
            "tags": ["Contacts"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/contact_id"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/Contact_coll1"}},
            "description": "Retrieve Contact from contact",
            "operationId": "RetrieveContactinstance_0",
        },
        "patch": {
            "tags": ["Contacts"],
            "parameters": [{"$ref": "#/components/parameters/contact_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/Contact"}
                    }
                },
                "description": "Contact attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "$ref": "#/components/responses/Contact_coll1",
                }
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
    "schemas": {
        "Contact": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "given_name": {"type": "string"},
                                "family_name": {"type": "string"},
                                "website": {"type": "string", "format": "url"},
                                "email": {"type": "string", "format": "email"},
                                "organization": {"type": "string"},
                                "orcid": {"type": "string"},
                            },
                        },
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                    },
                    "example": {
                        "attributes": {
                            "given_name": "",
                            "family_name": "",
                            "website": "",
                            "email": "",
                            "organization": "",
                            "orcid": "1234-1234-1234-1234",
                        },
                        "type": "Contact",
                        "id": "0",
                    },
                }
            },
            "description": "Contact Schema;",
        },
    },
    "responses": {
        "Contact_coll1": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "attributes": {
                                        "given_name": "",
                                        "family_name": "",
                                        "website": "",
                                        "email": "",
                                        "active": True,
                                        "organization": "",
                                        "orcid": "1234-1234-1234-1234",
                                    },
                                    "type": "Contact",
                                    "id": "0",
                                    "relationships": {
                                        "user": {"data": [], "links": {"self": None}}
                                    },
                                },
                                "type": "object",
                            }
                        },
                        "description": "Contact get;",
                    }
                }
            },
            "description": "Contact",
        },
    },
    "parameters": {
        "contact_id": {
            "name": "contact_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
}
