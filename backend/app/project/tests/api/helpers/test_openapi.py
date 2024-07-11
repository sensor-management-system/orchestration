# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test classes for openapi helpers."""

from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Relationship, Schema

from project.api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from project.tests.base import BaseTestCase


class TestMarshmallowJsonApiToOpenApiMapper(BaseTestCase):
    """Test the MarshmallowJsonApiToOpenApiMapper."""

    def setUp(self):
        """Create some test schema class that is used for mapping."""

        class TestSchema(Schema):
            """Test schema class for the device parameters."""

            class Meta:
                """Meta class for the TestSchema class."""

                type_ = "device_parameter"
                self_view = ("api.device_parameter_detail",)
                self_view_kwargs = {"id": "<id>"}

            id = fields.Integer(as_string=True)
            label = fields.Str(required=True)
            description = fields.Str(allow_none=True)
            unit_uri = fields.Str(allow_none=True)
            unit_name = fields.Str(allow_none=True)

            created_at = fields.DateTime(dump_only=True)
            updated_at = fields.DateTime(dump_only=True)
            group_ids = fields.Field(many=True, allow_none=True)

            device_id = fields.Integer(dump_only=True, load_only=True)
            device = Relationship(
                related_view="api.device_detail",
                related_view_kwargs={"id": "<device_id>"},
                include_resource_linkage=True,
                type_="device",
                schema="DeviceSchema",
                id_field="id",
            )

            created_by = Relationship(
                attribute="created_by",
                related_view="api.user_detail",
                related_view_kwargs={"id": "<created_by_id>"},
                include_resource_linkage=True,
                schema="UserSchema",
                type_="user",
                dump_only=True,
            )
            updated_by = Relationship(
                related_view="api.user_detail",
                related_view_kwargs={"id": "<updated_by_id>"},
                include_resource_linkage=True,
                schema="UserSchema",
                type_="user",
                dump_only=True,
            )

            device_parameter_value_change_actions = Relationship(
                related_view="api.device_parameter_value_change_action_list",
                related_view_kwargs={"id": "<id>"},
                include_resource_linkage=True,
                many=True,
                allow_none=True,
                schema="DeviceParameterValueChangeActionSchema",
                type_="device_parameter_value_change_action",
                id_field="id",
            )

        self.mapper = MarshmallowJsonApiToOpenApiMapper(TestSchema)

    def test_get_one(self):
        """Ensure the get_one method gives us a schema for one entry."""
        result = self.mapper.get_one()

        expected = {
            "schema": {
                "properties": {
                    "jsonapi": {
                        "type": "object",
                        "properties": {"version": {"type": "string", "default": "1.0"}},
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "type": {"type": "string", "default": "device_parameter"},
                            "attributes": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "description": {
                                        "type": "string",
                                    },
                                    "unit_uri": {
                                        "type": "string",
                                    },
                                    "unit_name": {"type": "string"},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                    },
                                    "updated_at": {
                                        "type": "string",
                                        "format": "date-time",
                                    },
                                    "group_ids": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                            },
                            "relationships": {
                                "type": "object",
                                "properties": {
                                    "device": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "type": {
                                                        "type": "string",
                                                        "default": "device",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    "created_by": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "type": {
                                                        "type": "string",
                                                        "default": "user",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    "updated_by": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "type": {
                                                        "type": "string",
                                                        "default": "user",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    "device_parameter_value_change_actions": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "string",
                                                        },
                                                        "type": {
                                                            "type": "string",
                                                            "default": "device_parameter_value_change_action",
                                                        },
                                                    },
                                                },
                                            }
                                        },
                                    },
                                },
                            },
                        },
                    },
                }
            }
        }
        self.assertEqual(result, expected)

    def test_get_list(self):
        """Ensure the get_list method gives us a schema for a list of entries."""
        result = self.mapper.get_list()

        expected = {
            "schema": {
                "properties": {
                    "jsonapi": {
                        "type": "object",
                        "properties": {"version": {"type": "string", "default": "1.0"}},
                    },
                    "meta": {
                        "type": "object",
                        "properties": {
                            "count": {"type": "number"},
                        },
                    },
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "type": {
                                    "type": "string",
                                    "default": "device_parameter",
                                },
                                "attributes": {
                                    "type": "object",
                                    "properties": {
                                        "label": {"type": "string"},
                                        "description": {
                                            "type": "string",
                                        },
                                        "unit_uri": {
                                            "type": "string",
                                        },
                                        "unit_name": {"type": "string"},
                                        "created_at": {
                                            "type": "string",
                                            "format": "date-time",
                                        },
                                        "updated_at": {
                                            "type": "string",
                                            "format": "date-time",
                                        },
                                        "group_ids": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                    },
                                },
                                "relationships": {
                                    "type": "object",
                                    "properties": {
                                        "device": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {"type": "string"},
                                                        "type": {
                                                            "type": "string",
                                                            "default": "device",
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "created_by": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {"type": "string"},
                                                        "type": {
                                                            "type": "string",
                                                            "default": "user",
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "updated_by": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {"type": "string"},
                                                        "type": {
                                                            "type": "string",
                                                            "default": "user",
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                        "device_parameter_value_change_actions": {
                                            "type": "object",
                                            "properties": {
                                                "data": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "string",
                                                            },
                                                            "type": {
                                                                "type": "string",
                                                                "default": "device_parameter_value_change_action",
                                                            },
                                                        },
                                                    },
                                                }
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                }
            }
        }
        self.assertEqual(result, expected)

    def test_post(self):
        """Ensure the post method gives us a schema for a post payload."""
        result = self.mapper.post()

        expected = {
            "schema": {
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "default": "device_parameter"},
                            "attributes": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "description": {
                                        "type": "string",
                                    },
                                    "unit_uri": {
                                        "type": "string",
                                    },
                                    "unit_name": {"type": "string"},
                                    "group_ids": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                                "required": ["label"],
                            },
                            "relationships": {
                                "type": "object",
                                "properties": {
                                    "device": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "type": {
                                                        "type": "string",
                                                        "default": "device",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    "device_parameter_value_change_actions": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "string",
                                                        },
                                                        "type": {
                                                            "type": "string",
                                                            "default": "device_parameter_value_change_action",
                                                        },
                                                    },
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
        self.assertEqual(result, expected)

    def test_patch(self):
        """Ensure the post method gives us a schema for a patch payload."""
        result = self.mapper.patch()
        expected = {
            "schema": {
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                            },
                            "type": {"type": "string", "default": "device_parameter"},
                            "attributes": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "description": {
                                        "type": "string",
                                    },
                                    "unit_uri": {
                                        "type": "string",
                                    },
                                    "unit_name": {"type": "string"},
                                    "group_ids": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                            },
                            "relationships": {
                                "type": "object",
                                "properties": {
                                    "device": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "type": {
                                                        "type": "string",
                                                        "default": "device",
                                                    },
                                                },
                                            },
                                        },
                                    },
                                    "device_parameter_value_change_actions": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "string",
                                                        },
                                                        "type": {
                                                            "type": "string",
                                                            "default": "device_parameter_value_change_action",
                                                        },
                                                    },
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
        self.assertEqual(result, expected)

    def test_filters(self):
        """Ensure we can extract the filters from the schema."""
        result = self.mapper.filters()

        expected = [
            {
                "name": "filter[id]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": "filter[label]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": "filter[description]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": "filter[unit_uri]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": "filter[unit_name]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": "filter[created_at]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string",
                    "format": "date-time",
                },
            },
            {
                "name": "filter[updated_at]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string",
                    "format": "date-time",
                },
            },
            {
                "name": "filter[device_id]",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "number",
                },
            },
        ]

        self.assertEqual(result, expected)
