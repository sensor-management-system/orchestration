"""Tests for the json schema dumper."""
from project.api.schemas.json_schema import JSONSchema
from project.api.schemas.role import ConfigurationRoleSchema
from project.tests.base import BaseTestCase


class TestJsonSchema(BaseTestCase):
    """Test case for the json schema dumper."""

    def test_configuration_role_schema(self):
        """Test with the configuration role schema."""
        role_schema = ConfigurationRoleSchema()
        json_schema = JSONSchema()
        dumped = json_schema.dump(role_schema)

        expected = {
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
                            "default": "configuration_contact_role",
                        },
                        "attributes": {
                            "type": "object",
                            "properties": {
                                "role_uri": {
                                    "type": "string",
                                },
                                "role_name": {
                                    "type": "string",
                                },
                            },
                        },
                        "relationships": {
                            "type": "object",
                            "properties": {
                                "contact": {
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
                                },
                                "configuration": {
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
                                },
                            },
                        },
                    },
                }
            },
        }
        self.assertEqual(dumped, expected)

    def test_configuration_role_schema_many(self):
        """Test with the configuration role schema for many."""
        role_schema = ConfigurationRoleSchema(many=True)
        json_schema = JSONSchema()
        dumped = json_schema.dump(role_schema)

        expected = {
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
                                "default": "configuration_contact_role",
                            },
                            "attributes": {
                                "type": "object",
                                "properties": {
                                    "role_uri": {
                                        "type": "string",
                                    },
                                    "role_name": {
                                        "type": "string",
                                    },
                                },
                            },
                            "relationships": {
                                "type": "object",
                                "properties": {
                                    "contact": {
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
                                    },
                                    "configuration": {
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
                                    },
                                },
                            },
                        },
                    },
                }
            },
        }
        self.assertEqual(dumped, expected)
