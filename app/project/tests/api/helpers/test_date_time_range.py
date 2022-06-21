"""Tests for the date_time_range module."""

import datetime

from project.api.helpers.date_time_range import DateTimeRange
from project.tests.base import BaseTestCase


class TestDateTimeRange(BaseTestCase):
    """Tests for the DateTimeRange class."""

    def test_no_overlap(self):
        """Test the simple case with start & end that don't overlap."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)
        end1 = datetime.datetime(year=2022, month=5, day=17)

        begin2 = datetime.datetime(year=2022, month=5, day=18)
        end2 = datetime.datetime(year=2022, month=5, day=19)

        range1 = DateTimeRange(begin1, end1)
        range2 = DateTimeRange(begin2, end2)

        self.assertFalse(range1.overlaps_with(range2))
        # We always want to make sure that the ordering of the operands
        # doesn't matter.
        self.assertFalse(range2.overlaps_with(range1))

    def test_simple_overlap(self):
        """Test the simple case with start & end that overlap."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)
        end1 = datetime.datetime(year=2022, month=5, day=18)

        begin2 = datetime.datetime(year=2022, month=5, day=17)
        end2 = datetime.datetime(year=2022, month=5, day=19)

        range1 = DateTimeRange(begin1, end1)
        range2 = DateTimeRange(begin2, end2)

        self.assertTrue(range1.overlaps_with(range2))
        self.assertTrue(range2.overlaps_with(range1))

    def test_simple_overlap_same_begin_date(self):
        """Test the case with same begin dates."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)
        end1 = datetime.datetime(year=2022, month=5, day=18)

        end2 = datetime.datetime(year=2022, month=5, day=19)

        range1 = DateTimeRange(begin1, end1)
        range2 = DateTimeRange(begin1, end2)

        self.assertTrue(range1.overlaps_with(range2))
        self.assertTrue(range2.overlaps_with(range1))

    def test_simple_overlap_single_point_in_time_same_begin_date(self):
        """Test the case with same begin dates & one span for a single point in time."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)

        end2 = datetime.datetime(year=2022, month=5, day=19)

        range1 = DateTimeRange(begin1, begin1)
        range2 = DateTimeRange(begin1, end2)

        self.assertTrue(range1.overlaps_with(range2))
        self.assertTrue(range2.overlaps_with(range1))

    def test_simple_overlap_single_point_in_time_different_begin_date(self):
        """Test the case with same begin dates & one span for a single point in time."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)

        begin2 = datetime.datetime(year=2022, month=2, day=15)
        end2 = datetime.datetime(year=2022, month=5, day=19)

        range1 = DateTimeRange(begin1, begin1)
        range2 = DateTimeRange(begin2, end2)

        self.assertTrue(range1.overlaps_with(range2))
        self.assertTrue(range2.overlaps_with(range1))

    def test_included(self):
        """Test with a date range that is included in another one."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)
        end1 = datetime.datetime(year=2022, month=5, day=19)

        begin2 = datetime.datetime(year=2022, month=5, day=17)
        end2 = datetime.datetime(year=2022, month=5, day=18)

        range1 = DateTimeRange(begin1, end1)
        range2 = DateTimeRange(begin2, end2)

        self.assertTrue(range1.overlaps_with(range2))
        self.assertTrue(range2.overlaps_with(range1))

    def test_direct_start(self):
        """Test with a direct start on the first ranges end (no overlap)."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)
        mid = datetime.datetime(year=2022, month=5, day=19)
        end2 = datetime.datetime(year=2022, month=5, day=20)

        range1 = DateTimeRange(begin1, mid)
        range2 = DateTimeRange(mid, end2)

        self.assertFalse(range1.overlaps_with(range2))
        self.assertFalse(range2.overlaps_with(range1))

    def test_undefined_end_non_overlap(self):
        """Test with undefined end date, but no overlap."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)
        end1 = datetime.datetime(year=2022, month=5, day=19)

        begin2 = datetime.datetime(year=2022, month=5, day=20)
        end2 = None

        range1 = DateTimeRange(begin1, end1)
        range2 = DateTimeRange(begin2, end2)

        self.assertFalse(range1.overlaps_with(range2))
        self.assertFalse(range2.overlaps_with(range1))

    def test_undefined_end_overlap(self):
        """Test with undefined end & an overlap."""
        begin1 = datetime.datetime(year=2022, month=5, day=16)
        end1 = None

        begin2 = datetime.datetime(year=2022, month=5, day=17)
        end2 = datetime.datetime(year=2022, month=5, day=19)

        range1 = DateTimeRange(begin1, end1)
        range2 = DateTimeRange(begin2, end2)

        self.assertTrue(range1.overlaps_with(range2))
        self.assertTrue(range2.overlaps_with(range1))

    def test_construct_with_earlier_end_date(self):
        """Test that we throw an ValueError if begin is after end."""
        begin1 = datetime.datetime(year=2022, month=5, day=19)
        end1 = datetime.datetime(year=2022, month=5, day=16)

        with self.assertRaises(ValueError):
            DateTimeRange(begin1, end1)
