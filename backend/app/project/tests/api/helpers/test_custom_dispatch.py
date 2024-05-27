# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the custom dispatch decorator."""

from project.api.helpers.custom_dispatch import custom_dispatch
from project.tests.base import BaseTestCase


@custom_dispatch
def to_string(x):
    """Return a string representation of the element, depending on type."""
    return type(x)


@to_string.default
def to_string(x):
    """Return a default string representation."""
    return "None"


@to_string.register(str)
def to_string(x):
    """Return a string representation for strings."""
    return f"str({repr(x)})"


@to_string.register(int)
def to_string(x):
    """Return a string representation for integers."""
    return f"int({x})"


to_string.register_same(float, handler=int)


class TestCustomDispatch(BaseTestCase):
    """Test class to check the custom_dispatch function."""

    def test_dispatch_by_type(self):
        """Check the dispatch by explicitly registered type."""
        self.assertEqual(to_string("Something"), "str('Something')")
        self.assertEqual(to_string(23), "int(23)")

    def test_default(self):
        """Check the default function."""
        self.assertEqual(to_string(None), "None")
        self.assertEqual(to_string({"key": "value"}), "None")

    def test_register_same(self):
        """Check the dispatch by functions added with register_same."""
        self.assertEqual(to_string(42.2), "int(42.2)")

    def test_find_for(self):
        """Check that we can find the function that will be used for a type."""
        f = to_string.find_for(str)
        self.assertEqual(f(42), "str(42)")

    def test_find_for_default(self):
        """Ensure we get the default funciton if we we don't have an explicit registered function."""
        f = to_string.find_for(dict)
        self.assertEqual(f(42), "None")

    def test_deletage(self):
        """Check that we can delegate to another function."""
        self.assertEqual(to_string.delegate(str, 42), "str(42)")

    def test_deletage_for_default(self):
        """Check that we can delegate to the default function."""
        self.assertEqual(to_string.delegate(dict, 42), "None")
