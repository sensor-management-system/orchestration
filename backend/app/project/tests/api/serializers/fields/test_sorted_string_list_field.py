# SPDX-FileCopyrightText: 2026
# - Rubankumar Moorthy <r.moorthy@fz-juelich.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Research Centre Juelich GmbH - Institute of Bio- and Geosciences Agrosphere (IBG-3,
#   https://www.fz-juelich.de/en/ibg/ibg-3)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the sorted string list field."""

from argparse import Namespace
from unittest import TestCase

from flask_rest_jsonapi.schema import get_nested_fields
from marshmallow import ValidationError

from project.api.serializer.fields.sorted_string_list_field import SortedStringListField


class TestSortedStringListField(TestCase):
    """Tests for the SortedStringListField."""

    def setUp(self):
        """Set up the field under test."""
        self.field = SortedStringListField(allow_none=True)

    def test_deserialize_sorts_strings_case_insensitively(self):
        """Ensure incoming strings are sorted without changing their spelling."""
        result = self.field.deserialize(["water depth", "GPS", "Atmos"])

        self.assertEqual(["Atmos", "GPS", "water depth"], result)

    def test_deserialize_none(self):
        """Ensure None is accepted when configured via allow_none."""
        self.assertIsNone(self.field.deserialize(None))

    def test_deserialize_rejects_a_string(self):
        """Ensure a string is not split into individual characters."""
        with self.assertRaises(ValidationError):
            self.field.deserialize("keyword")

    def test_deserialize_rejects_non_string_items(self):
        """Ensure every item in the incoming list must be a string."""
        with self.assertRaises(ValidationError):
            self.field.deserialize(["keyword", 42])

    def test_serialize_sorts_strings_case_insensitively(self):
        """Ensure stored strings are sorted in API output."""
        model = Namespace(keywords=["water depth", "GPS", "Atmos"])

        result = self.field.serialize("keywords", model)

        self.assertEqual(["Atmos", "GPS", "water depth"], result)

    def test_serialize_none(self):
        """Ensure None remains None in API output."""
        model = Namespace(keywords=None)

        self.assertIsNone(self.field.serialize("keywords", model))

    def test_is_not_mistaken_for_a_nested_relationship(self):
        """Ensure flask-rest-jsonapi can inspect schemas containing the field."""
        schema = Namespace(_declared_fields={"keywords": self.field})

        self.assertEqual([], get_nested_fields(schema))
