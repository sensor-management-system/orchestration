# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Helper classes to work with the openapi."""

from marshmallow import fields
from marshmallow_jsonapi.flask import Relationship


class MarshmallowJsonApiToOpenApiMapper:
    """Mapper to extract the openapi schema of a Marshmallow schema."""

    def __init__(self, schema):
        """Init the mapper with a schema."""
        self.schema = schema

    def _field_to_openapi_type(self, field):
        """Return the type information for a specific field."""
        if getattr(field, "as_string", False):
            return {"type": "string"}
        if isinstance(field, fields.Str):
            return {"type": "string"}
        if isinstance(field, fields.DateTime):
            return {"type": "string", "format": "date-time"}
        if isinstance(field, fields.Int):
            return {"type": "number"}
        if isinstance(field, fields.Float):
            return {"type": "number"}
        if isinstance(field, fields.Boolean):
            return {"type": "boolean"}
        if isinstance(field, Relationship):
            if getattr(field, "many", False):
                return {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "type": {"type": "string", "default": field.type_},
                                },
                            },
                        }
                    },
                }
            return {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "type": {"type": "string", "default": field.type_},
                        },
                    }
                },
            }
        if isinstance(
            field, fields.Field
        ):  # and getattr(field, "many", False) is True:
            return {"type": "array", "items": {"type": "string"}}
        raise NotImplementedError(f"fieldtype unknown: {field}")

    def get_one(self):
        """Extact the openapi schema to get one entry."""
        attribute_properties = {}
        relationship_properties = {}
        id_property = {}

        for name, field in self.schema._declared_fields.items():
            load_only = getattr(field, "load_only", False)
            if not load_only:
                if name == "id":
                    id_property = {"id": self._field_to_openapi_type(field)}
                elif isinstance(field, Relationship):
                    relationship_properties[name] = self._field_to_openapi_type(field)
                else:
                    attribute_properties[name] = self._field_to_openapi_type(field)
        properties = {
            "data": {
                "type": "object",
                "properties": {
                    **id_property,
                    "type": {"type": "string", "default": self.schema.Meta.type_},
                    "attributes": {
                        "type": "object",
                        "properties": attribute_properties,
                    },
                    "relationships": {
                        "type": "object",
                        "properties": relationship_properties,
                    },
                },
            },
            "jsonapi": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "string",
                        "default": "1.0",
                    }
                },
            },
        }
        return {"schema": {"properties": properties}}

    def get_list(self):
        """Extract the openapi schema to get a list of entries."""
        attribute_properties = {}
        relationship_properties = {}
        id_property = {}

        for name, field in self.schema._declared_fields.items():
            load_only = getattr(field, "load_only", False)
            if not load_only:
                if name == "id":
                    id_property = {"id": self._field_to_openapi_type(field)}
                elif isinstance(field, Relationship):
                    relationship_properties[name] = self._field_to_openapi_type(field)
                else:
                    attribute_properties[name] = self._field_to_openapi_type(field)

        properties = {
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        **id_property,
                        "type": {"type": "string", "default": self.schema.Meta.type_},
                        "attributes": {
                            "type": "object",
                            "properties": attribute_properties,
                        },
                        "relationships": {
                            "type": "object",
                            "properties": relationship_properties,
                        },
                    },
                },
            },
            "meta": {
                "type": "object",
                "properties": {
                    "count": {
                        "type": "number",
                    }
                },
            },
            "jsonapi": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "string",
                        "default": "1.0",
                    }
                },
            },
        }
        return {"schema": {"properties": properties}}

    def post(self):
        """Extract the openapi schema to handle a post request body."""
        attribute_properties = {}
        relationship_properties = {}

        required_attributes = []
        for name, field in self.schema._declared_fields.items():
            if name == "id" or getattr(field, "dump_only", False):
                continue
            if isinstance(field, Relationship):
                relationship_properties[name] = self._field_to_openapi_type(field)
            else:
                attribute_properties[name] = self._field_to_openapi_type(field)
                if getattr(field, "required", False):
                    required_attributes.append(name)

        properties = {
            "data": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "default": self.schema.Meta.type_},
                    "attributes": {
                        "type": "object",
                        "properties": attribute_properties,
                        "required": required_attributes,
                    },
                    "relationships": {
                        "type": "object",
                        "properties": relationship_properties,
                    },
                },
            }
        }
        return {"schema": {"properties": properties}}

    def patch(self):
        """Extract the openapi schema to handle a patch request body."""
        attribute_properties = {}
        relationship_properties = {}
        id_property = {}

        for name, field in self.schema._declared_fields.items():
            if name == "id":
                id_property = {"id": self._field_to_openapi_type(field)}
                continue
            if getattr(field, "dump_only", False):
                continue
            if isinstance(field, Relationship):
                relationship_properties[name] = self._field_to_openapi_type(field)
            else:
                attribute_properties[name] = self._field_to_openapi_type(field)

        properties = {
            "data": {
                "type": "object",
                "properties": {
                    **id_property,
                    "type": {"type": "string", "default": self.schema.Meta.type_},
                    "attributes": {
                        "type": "object",
                        "properties": attribute_properties,
                    },
                    "relationships": {
                        "type": "object",
                        "properties": relationship_properties,
                    },
                },
            }
        }
        return {"schema": {"properties": properties}}

    def filters(self):
        result = []
        for name, field in self.schema._declared_fields.items():
            if isinstance(field, Relationship):
                continue
            type_information = self._field_to_openapi_type(field)
            if type_information["type"] != "array":
                one_filter = {
                    "name": f"filter[{name}]",
                    "in": "query",
                    # As those are all filters, all of them are optional.
                    "required": False,
                    "schema": type_information,
                }
                result.append(one_filter)

        return result
