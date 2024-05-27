# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test cases for the memorize function."""

from unittest import TestCase
from unittest.mock import patch

from project.api.helpers.memorize import memorize


class Console:
    """A dummy object that we can mock."""

    def log(self, txt):
        """Log text to stdout."""
        print(txt)


console = Console()


class SpecialException(Exception):
    """A dummy exception that we can raise."""

    pass


class A:
    """A base class to test the memorize decorator with inheritance."""

    @classmethod
    @memorize
    def m1(cls):
        """
        Return a list of entries based on a class method in the sub classes.

        Should be memorized, but only on the sub class level.
        (So memorized for B1 and B2 with their associated results).
        """
        return list(cls.m2().keys())


class B1(A):
    """Child class 1 to test the memorization of m1."""

    @classmethod
    def m2(cls):
        """Return a dict."""
        console.log("b1")
        return {"b1": True}


class B2(A):
    """Child class 2 to test the memorization of m1."""

    @classmethod
    def m2(cls):
        """Return a dict."""
        console.log("b2")
        return {"b2": False}


class TestOnce(TestCase):
    """Test class for the memorize function."""

    def test_memorize(self):
        """Ensure we memorize the result with the memorize function."""

        @memorize
        def my_test_function():
            """Run some test code."""
            console.log("hi there")
            return 42

        with patch.object(console, "log") as log:
            log.return_value = None
            result1 = my_test_function()
            result2 = my_test_function()

            self.assertEqual(result1, result2)
            self.assertEqual(result1, 42)
            # We called the log only once. No second call for the second run.
            log.assert_called_once()

    def test_memorize_with_exception(self):
        """Ensure that we don't store results if there is an exception."""

        @memorize
        def my_test_function():
            """Run some test code."""
            console.log("hi there")
            return 42

        with patch.object(console, "log") as log:
            log.side_effect = SpecialException("no")
            with self.assertRaises(SpecialException):
                my_test_function()
            with self.assertRaises(SpecialException):
                my_test_function()

            # Now we run the log function again.
            self.assertEqual(log.call_count, 2)

    def test_memorize_with_classmethods(self):
        """Ensure we handle class methods on the level we on which we call them."""
        with patch.object(console, "log") as log:
            log.return_value = None
            result1 = B1.m1()
            result2 = B2.m1()

            self.assertEqual(result1, ["b1"])
            self.assertEqual(result2, ["b2"])

            for i in range(100):
                B1.m1()
                B2.m1()

            self.assertEqual(log.call_count, 2)
