# SPDX-FileCopyrightText: 2020 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

components = {
    "schemas": {
        "conflict": {
            "type": "object",
            "properties": {
                "errors": {
                    "example": [
                        {
                            "status": "409",
                            "source": "",
                            "title": "Conflict"
                        }
                    ],
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string"
                            },
                            "source": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            }
                        }
                    }
                },
                "jsonapi": {
                    "example": {
                        "version": "1.0"
                    },
                    "type": "object",
                    "properties": {
                        "version": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "authentification_required": {
            "type": "object",
            "properties": {
                "errors": {
                    "example": [
                        {
                            "status": "401",
                            "source": "Authentification required.",
                            "title": "Unauthorized",
                        }
                    ],
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "source": {"type": "string"},
                            "title": {"type": "string"},
                        },
                    },
                },
                "jsonapi": {
                    "example": {"version": "1.0"},
                    "type": "object",
                    "properties": {"version": {"type": "string"}},
                },
            },
        },
        "invalid_filters": {
            "type": "object",
            "properties": {
                "errors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "detail": {
                                "type": "string",
                            },
                            "status": {
                                "type": "string",
                            },
                            "title": {
                                "type": "string",
                            },
                        },
                    },
                    "example": [
                        {
                            "detail": "Parse error",
                            "status": "400",
                            "title": "Invalid filters querystring parameter",
                        }
                    ],
                },
                "jsonapi": {
                    "example": {
                        "version": "1.0",
                    },
                    "type": "object",
                    "properties": {"version": {"type": "string"}},
                },
            },
        },
    },
}
