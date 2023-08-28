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
