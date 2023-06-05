components = {
    "schemas": {
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
