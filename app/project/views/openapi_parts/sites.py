"""External openapi spec file for the sites endpoints."""

paths = {
    "/sites": {
        "get": {
            "tags": ["Sites"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                {"$ref": "#/components/parameters/created_at"},
                {"$ref": "#/components/parameters/updated_at"},
                {"$ref": "#/components/parameters/start_date"},
                {"$ref": "#/components/parameters/end_date"},
                {"$ref": "#/components/parameters/label"},
                {"$ref": "#/components/parameters/status"},
                {"$ref": "#/components/parameters/created_by_id"},
                {"$ref": "#/components/parameters/updated_by_id"},
                {"$ref": "#/components/parameters/id"},
                {"$ref": "#/components/parameters/filter"},
                {"$ref": "#/components/parameters/hide_archived"},
            ],
            "responses": {"200": {"$ref": "#/components/responses/Site_coll"}},
            "description": "Retrieve Site from site",
            "operationId": "RetrieveacollectionofSiteobjects_0",
        },
        "post": {
            "tags": ["Sites"],
            "description": "create a Site",
            "requestBody": {"$ref": "#/components/requestBodies/Site_inst"},
            "responses": {"201": {"$ref": "#/components/responses/Site_inst"}},
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
            "responses": {"200": {"$ref": "#/components/responses/Site_inst"}},
            "description": "Retrieve Site from site",
            "operationId": "RetrieveSiteinstance_0",
        },
        "patch": {
            "tags": ["Sites"],
            "parameters": [{"$ref": "#/components/parameters/site_id"}],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/Site"}
                    }
                },
                "description": "Site attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Request fulfilled, document follows",
                    "content": {
                        "application/vnd.api+json": {
                            "schema": {"$ref": "#/components/responses/Site_inst"}
                        }
                    },
                }
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
    "/sites/{site_id}/archive": {
        "post": {
            "tags": ["Sites"],
            "parameters": [
                {"$ref": "#/components/parameters/site_id"},
            ],
            "responses": {
                "204": {"description": "Site was archived succesfully."},
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
                "409": {"$ref": "#/components/errors/conflict"},
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
                "401": {"$ref": "#/components/errors/authentification_required"},
                "403": {"$ref": "#/components/responses/jsonapi_error_403"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Restore an archived site.",
            "operationId": "RestoreSite",
        }
    },
}
components = {
    "responses": {
        "Site_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": [
                                    {
                                        "attributes": {
                                            "created_at": "2022-08-31T12:00:00",
                                            "updated_at": "2022-08-31T12:00:00",
                                            "label": "test cfg",
                                            "geometry": "POLYGON ((10 10, 10 20, 20 20, 20 10, 10 10))",
                                            "description": "some description",
                                            "epsg_code": "4326",
                                            "street": "Main street",
                                            "street_number": "123d",
                                            "city": "Hometown",
                                            "zip_code": "11111",
                                            "country": "Far away",
                                            "building": "A70",
                                            "room": "left",
                                            "groups_ids": ["1", "2", "3"],
                                            "is_public": False,
                                            "is_internal": True,
                                            "archived": False,
                                            "elevation_datum_name": "MSL",
                                            "elevation_datum_uri": "https://cv/elevation/123",
                                            "elevation": 42.0,
                                            "site_type_name": "example site",
                                            "site_type_uri": "https://cv/sites/345",
                                            "site_usage_name": "example usage",
                                            "site_usage_uri": "https://cv/usages/345",
                                        },
                                        "type": "site",
                                        "id": "0",
                                        "relationships": {
                                            "created_by": {
                                                "data": {
                                                    "id": "1",
                                                    "type": "user",
                                                },
                                            },
                                            "updated_by": {
                                                "data": {
                                                    "id": "1",
                                                    "type": "user",
                                                },
                                            },
                                        },
                                    }
                                ],
                                "type": "string",
                            }
                        },
                        "description": "Site get;",
                    }
                }
            },
            "description": "Request fulfilled, document follows",
        },
        "Site_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "attributes": {
                                        "created_at": "2022-08-31T12:00:00",
                                        "updated_at": "2022-08-31T12:00:00",
                                        "label": "test cfg",
                                        "geometry": "POLYGON ((10 10, 10 20, 20 20, 20 10, 10 10))",
                                        "description": "some description",
                                        "epsg_code": "4326",
                                        "street": "Main street",
                                        "street_number": "123d",
                                        "city": "Hometown",
                                        "zip_code": "11111",
                                        "country": "Far away",
                                        "building": "A70",
                                        "room": "left",
                                        "groups_ids": ["1", "2", "3"],
                                        "is_public": False,
                                        "is_internal": True,
                                        "archived": False,
                                        "elevation_datum_name": "MSL",
                                        "elevation_datum_uri": "https://cv/elevation/123",
                                        "elevation": 42.0,
                                        "site_type_name": "example site",
                                        "site_type_uri": "https://cv/sites/345",
                                        "site_usage_name": "example usage",
                                        "site_usage_uri": "https://cv/usages/345",
                                    },
                                    "type": "site",
                                    "id": "0",
                                    "relationships": {
                                        "created_by": {
                                            "data": {
                                                "id": "1",
                                                "type": "user",
                                            },
                                        },
                                        "updated_by": {
                                            "data": {
                                                "id": "1",
                                                "type": "user",
                                            },
                                        },
                                    },
                                },
                                "type": "string",
                            }
                        },
                        "description": "Site get;",
                    }
                }
            },
            "description": "Request fulfilled, document follows",
        },
    },
    "requestBodies": {
        "Site_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "label": {"type": "string"},
                                            "geometry": {"type": "string"},
                                            "description": {"type": "string"},
                                            "epsg_code": {"type": "string"},
                                            "street": {"type": "string"},
                                            "street_number": {"type": "string"},
                                            "city": {"type": "string"},
                                            "zip_code": {"type": "string"},
                                            "country": {"type": "string"},
                                            "building": {"type": "string"},
                                            "room": {"type": "string"},
                                            "group_ids": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                            "is_internal": {"type": "boolean"},
                                            "is_public": {"type": "boolean"},
                                            "archived": {"type": "boolean"},
                                            "elevation": {"type": "number"},
                                            "elevation_datum_uri": {
                                                "type": "string",
                                            },
                                            "elevation_datum_name": {
                                                "type": "string",
                                            },
                                            "site_type_uri": {
                                                "type": "string",
                                            },
                                            "site_type_name": {
                                                "type": "string",
                                            },
                                            "site_usage_uri": {
                                                "type": "string",
                                            },
                                            "site_usage_name": {
                                                "type": "string",
                                            },
                                        },
                                    }
                                },
                                "example": {
                                    "attributes": {
                                        "label": "test cfg",
                                        "geometry": "POLYGON ((10 10, 10 20, 20 20, 20 10, 10 10))",
                                        "description": "some description",
                                        "epsg_code": "4326",
                                        "street": "Main street",
                                        "street_number": "123d",
                                        "city": "Hometown",
                                        "zip_code": "11111",
                                        "country": "Far away",
                                        "building": "A70",
                                        "room": "left",
                                        "groups_ids": ["1", "2", "3"],
                                        "is_public": False,
                                        "is_internal": True,
                                        "elevation_datum_name": "MSL",
                                        "elevation_datum_uri": "https://cv/elevation/123",
                                        "elevation": 42.0,
                                        "site_type_name": "example site",
                                        "site_type_uri": "https://cv/sites/345",
                                        "site_usage_name": "example usage",
                                        "site_usage_uri": "https://cv/usages/345",
                                    },
                                    "type": "site",
                                },
                            }
                        },
                        "description": "Site patch;Site post;Site delete;Site patch;Site post;Site delete;",
                    }
                }
            }
        },
    },
    "parameters": {
        "site_id": {
            "name": "site_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        },
    },
    "schemas": {
        "Site": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "geometry": {"type": "string"},
                                "description": {"type": "string"},
                                "epsg_code": {"type": "string"},
                                "street": {"type": "string"},
                                "street_number": {"type": "string"},
                                "city": {"type": "string"},
                                "zip_code": {"type": "string"},
                                "country": {"type": "string"},
                                "building": {"type": "string"},
                                "room": {"type": "string"},
                                "group_ids": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "is_internal": {"type": "boolean"},
                                "is_public": {"type": "boolean"},
                                "archived": {"type": "boolean"},
                                "elevation": {"type": "number"},
                                "elevation_datum_uri": {
                                    "type": "string",
                                },
                                "elevation_datum_name": {
                                    "type": "string",
                                },
                                "site_type_uri": {
                                    "type": "string",
                                },
                                "site_type_name": {
                                    "type": "string",
                                },
                                "site_usage_uri": {
                                    "type": "string",
                                },
                                "site_usage_name": {
                                    "type": "string",
                                },
                            },
                        },
                        "relationships": {
                            "type": "object",
                            "properties": {
                                "created_by": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "string",
                                                },
                                                "type": {
                                                    "type": "string",
                                                    "default": "user",
                                                },
                                            },
                                        }
                                    },
                                },
                                "updated_by": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "string",
                                                },
                                                "type": {
                                                    "type": "string",
                                                    "default": "user",
                                                },
                                            },
                                        }
                                    },
                                },
                            },
                        },
                    },
                    "example": {
                        "id": "0",
                        "attributes": {
                            "created_at": "2022-08-31T12:00:00",
                            "updated_at": "2022-08-31T12:00:00",
                            "label": "test cfg",
                            "geometry": "POLYGON ((10 10, 10 20, 20 20, 20 10, 10 10))",
                            "description": "some description",
                            "epsg_code": "4326",
                            "street": "Main street",
                            "street_number": "123d",
                            "city": "Hometown",
                            "zip_code": "11111",
                            "country": "Far away",
                            "building": "A70",
                            "room": "left",
                            "groups_ids": ["1", "2", "3"],
                            "is_public": False,
                            "is_internal": True,
                            "archived": False,
                            "elevation_datum_name": "MSL",
                            "elevation_datum_uri": "https://cv/elevation/123",
                            "elevation": 42.0,
                            "site_type_name": "example site",
                            "site_type_uri": "https://cv/sites/345",
                            "site_usage_name": "example usage",
                            "site_usage_uri": "https://cv/usages/345",
                        },
                        "type": "site",
                        "relationships": {
                            "created_by": {
                                "data": {
                                    "id": "1",
                                    "type": "user",
                                },
                            },
                            "updated_by": {
                                "data": {
                                    "id": "1",
                                    "type": "user",
                                },
                            },
                        },
                    },
                }
            },
            "description": "Site Schema;",
        },
    },
}
