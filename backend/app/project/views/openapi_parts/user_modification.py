# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Paths & components to describe the endpoints to modify user data."""

paths = {
    "/revoke-apikey": {
        "post": {
            "description": "Revoke the current apikey for the current user and generate a new one.",
            "tags": ["User"],
            "parameters": [],
            "responses": {
                "200": {"$ref": "#/components/responses/RevokeApikey"},
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
            "requestBody": {"$ref": "#/components/requestBodies/RevokeApikey"},
        }
    },
    "/accept-terms-of-use": {
        "post": {
            "description": "Update the date on which the user accepted the terms.",
            "tags": ["User"],
            "parameters": [],
            "responses": {
                "200": {"$ref": "#/components/responses/AcceptTermsOfUse"},
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
            "requestBody": {"$ref": "#/components/requestBodies/AcceptTermsOfUse"},
        }
    },
}
components = {
    "requestBodies": {
        "RevokeApikey": {
            "description": "Payload to revoke apikeys",
            "content": {"application/vnd.api+json": {"schema": {"properties": {}}}},
        },
        "AcceptTermsOfUse": {
            "description": "Payload to accept the terms of use",
            "content": {"application/vnd.api+json": {"schema": {"properties": {}}}},
        },
    },
    "responses": {
        "RevokeApikey": {
            "description": "Updated apikey",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "user",
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {"apikey": {"type": "string"}},
                                    },
                                },
                                "example": {
                                    "type": "user",
                                    "id": "1234",
                                    "attributes": {"apikey": "234567..."},
                                },
                            }
                        }
                    }
                }
            },
        },
        "AcceptTermsOfUse": {
            "description": "Updated terms of use aggrement date.",
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "user",
                                    },
                                    "id": {
                                        "type": "string",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "terms_of_use_agreement_date": {
                                                "type": "string",
                                                "format": "date-time",
                                            }
                                        },
                                    },
                                },
                                "example": {
                                    "type": "user",
                                    "id": "1234",
                                    "attributes": {
                                        "terms_of_use_agreement_date": "1970-01-01T00:00:00+00:00"
                                    },
                                },
                            }
                        }
                    }
                }
            },
        },
    },
}
