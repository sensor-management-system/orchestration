# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Externalized openapi spec for the static location actions."""
from ... import api
from ...api.resources import (
    ConfigurationStaticLocationBeginActionDetail,
    ConfigurationStaticLocationBeginActionList,
)


class ApiInspector:
    """
    Helper class to inspect the api object.

    Helps to extract resources & their urls.
    """

    def __init__(self, api):
        """Init the object."""
        self.api = api

    def find_registered_resource(self, registered_resource):
        """Find a registered resource with its urls or None."""
        for resource in api.resources:
            if resource["resource"] == registered_resource:
                return resource
        return None


inspector = ApiInspector(api)
# Here we are going to start to generate the spec from the
# resources that we already have.
list_resource = inspector.find_registered_resource(
    ConfigurationStaticLocationBeginActionList
)
# We can have multiple ones that could have more path parameters:
# /static-location/actions and
# /configurations/<int:configuration_id>/static-location-actions
#
# First one is the more general one without further parameters.
url_list_endpoint = list_resource["urls"][0]

detail_resource = inspector.find_registered_resource(
    ConfigurationStaticLocationBeginActionDetail
)

# The id parameter for the detail view doesn't follow the conventions
# that we use in the openapi spec - so we replace it.
url_detail_endpoint = detail_resource["urls"][0].replace(
    "<int:id>", "{static_location_action_id}"
)

# Other things that we could read from the resources are possible status
# codes, descriptions, ...

paths = {
    url_list_endpoint: {
        "get": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/StaticLocationAction_coll"}
            },
            "description": "Get the list of static location actions.",
        },
        "post": {
            "tags": ["Static location actions"],
            "requestBody": {
                "$ref": "#/components/requestBodies/StaticLocationAction_inst"
            },
            "responses": {
                "201": {"$ref": "#/components/responses/StaticLocationAction_coll"}
            },
        },
    },
    url_detail_endpoint: {
        "get": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/static_location_action_id"},
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/StaticLocationAction_coll"}
            },
        },
        "patch": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/static_location_action_id"}
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": {
                        "schema": {"$ref": "#/components/schemas/StaticLocationAction"}
                    }
                },
                "description": "",
                "required": True,
            },
            "responses": {
                "201": {"$ref": "#/components/responses/StaticLocationAction_coll"}
            },
        },
        "delete": {
            "tags": ["Static location actions"],
            "parameters": [
                {"$ref": "#/components/parameters/static_location_action_id"}
            ],
            "responses": {"200": {"$ref": "#/components/responses/object_deleted"}},
        },
    },
}
# We can also go on & inspect the schema, so that we could generate
# the requestBodies & responses.
# But we need further checks if the field is the id field (should
# not be part of the attributes) or if it is an relationship field
# (has an extra place - in the relationships dict).
detail_schema = ConfigurationStaticLocationBeginActionDetail.schema()
required_attributes_for_request_body = []
for field_name in ["begin_date"]:
    field = detail_schema.fields[field_name]
    if field.required:
        required_attributes_for_request_body.append(field_name)

components = {
    "requestBodies": {
        "StaticLocationAction_inst": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "default": "configuration_static_location_action",
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "properties": {
                                            "begin_description": {"type": "string"},
                                            "end_description": {"type": "string"},
                                            "label": {"type": "string"},
                                            "x": {"type": "number", "format": "float"},
                                            "y": {"type": "number", "format": "float"},
                                            "z": {"type": "number", "format": "float"},
                                            "epsg_code": {
                                                "type": "string",
                                                "default": "4326",
                                            },
                                            "elevation_datum_name": {
                                                "type": "string",
                                                "default": "MSL",
                                            },
                                            "elevation_datum_uri": {
                                                "type": "string",
                                                "format": "uri",
                                            },
                                            "begin_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                            "end_date": {
                                                "type": "string",
                                                "format": "datetime",
                                            },
                                        },
                                    },
                                    "relationships": {
                                        "type": "object",
                                        "properties": {
                                            "begin_contact": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "contact",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "end_contact": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "contact",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                            "configuration": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "object",
                                                        "properties": {
                                                            "type": {
                                                                "type": "string",
                                                                "default": "configuration",
                                                            },
                                                            "id": {"type": "string"},
                                                        },
                                                    }
                                                },
                                            },
                                        },
                                    },
                                },
                            }
                        }
                    }
                }
            }
        }
    },
    "responses": {
        "StaticLocationAction_coll": {
            "content": {
                "application/vnd.api+json": {
                    "schema": {
                        "properties": {
                            "data": {
                                "example": {
                                    "id": "0",
                                    "type": "configuration_static_location_action",
                                    "attributes": {
                                        "begin_description": "",
                                        "end_description": "",
                                        "label": "",
                                        "begin_date": "",
                                        "end_date": "",
                                        "epsg_code": "",
                                        "elevation_datum_name": "",
                                        "elevation_datum_uri": "",
                                        "x": 0,
                                        "y": 0,
                                        "z": 0,
                                    },
                                    "relationships": {
                                        "configuration": {
                                            "data": {
                                                "type": "configuration",
                                                "id": "00",
                                            }
                                        },
                                        "begin_contact": {
                                            "data": {"type": "contact", "id": "000"}
                                        },
                                        "end_contact": {
                                            "data": {"type": "contact", "id": "123"}
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "description": "",
        }
    },
    "parameters": {
        "static_location_action_id": {
            "name": "static_location_action_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
    "schemas": {
        "StaticLocationAction": {
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "default": "configuration_static_location_begin_action",
                        },
                        "id": {"type": "string"},
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "begin_description": {"type": "string"},
                                "end_description": {"type": "string"},
                                "label": {"type": "string"},
                                "x": {"type": "number", "format": "float"},
                                "y": {"type": "number", "format": "float"},
                                "z": {"type": "number", "format": "float"},
                                "epsg_code": {"type": "string", "default": "4326"},
                                "elevation_datum_name": {
                                    "type": "string",
                                    "default": "MSL",
                                },
                                "elevation_datum_uri": {
                                    "type": "string",
                                    "format": "uri",
                                },
                                "begin_date": {"type": "string", "format": "datetime"},
                                "end_date": {"type": "string", "format": "datetime"},
                            },
                        },
                        "relationships": {
                            "type": "object",
                            "properties": {
                                "begin_contact": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "contact",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                                "end_contact": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "contact",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                                "configuration": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "default": "configuration",
                                                },
                                                "id": {"type": "string"},
                                            },
                                        }
                                    },
                                },
                            },
                        },
                    },
                }
            },
            "description": "Static Location Action Schema;",
        }
    },
}
