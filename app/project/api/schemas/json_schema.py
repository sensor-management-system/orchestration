# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Helper class to dump json schemas for our marshmallow schemas."""

from marshmallow_jsonapi import fields


class JSONSchema:
    """
    Class to extract the json schema structure for our marshmallow schemas.

    Be careful, this class is work in progress.
    """

    def dump(self, schema):
        """Return the dict with the json schema structure."""
        attributes = {}
        relationships = {}

        id_field_name = "id"
        attribute_type_lookup = {
            fields.Str: "string",
        }
        for field_name, field in schema._declared_fields.items():
            is_attribute = False
            is_relationship = False
            type_ = None
            if getattr(field, "as_string", False):
                type_ = "string"

            if field_name == id_field_name:
                pass
            elif type(field) in attribute_type_lookup.keys():
                is_attribute = True
                type_ = attribute_type_lookup[type(field)]
            else:
                is_relationship = True

            if is_attribute:
                attributes[field_name] = {"type": type_}
            if is_relationship:
                relationships[field_name] = {
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
                                },
                            },
                        }
                    },
                }
        data_items = {
            "type": "object",
            "properties": {
                id_field_name: {
                    "type": "string",
                },
                "type": {
                    "type": "string",
                    "default": schema.Meta.type_,
                },
                "attributes": {
                    "type": "object",
                    "properties": attributes,
                },
                "relationships": {
                    "type": "object",
                    "properties": relationships,
                },
            },
        }
        if not schema.many:
            return {
                "type": "object",
                "properties": {
                    "data": data_items,
                },
            }
        return {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": data_items,
                }
            },
        }
