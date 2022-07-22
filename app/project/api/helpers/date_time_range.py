"""Datetime range tools."""


class DateTimeRange:
    """A class to represent a range of datetimes."""

    def __init__(self, begin_date, end_date=None):
        """
        Init the object with begin & end dates.

        The end date is optional & the class handles the
        overlapping tests for that as well.
        If the end date is None, it means that there is no
        end date defined & the time range never ends.
        (This is useful to handle time ranges for that the
        end date is still unknown.)

        :param datetime.datetime begin_date: param_begin_date
        :param datetime.datetime end_date: param_end_date
        """
        self.begin_date = begin_date
        self.end_date = end_date

        # Just to make sure that the begin_date is before the end_date
        if self.begin_date is not None and self.end_date is not None:
            if self.begin_date > self.end_date:
                raise ValueError("end_date should not be before begin_date")

    def overlaps_with(self, other_range):
        """
        Return true if there is an overlap of the two time ranges.

        This handles cases in that the end date is unknown, simulating
        never ending usage.
        This method also makes sure that it works no matter which ordering
        the operands have.

        An end of the current range that is identical with the start
        of the next time range, is not seen as an overlap.
        (For sensors we stop one mount in one point & can go on with the
        device in another mount right away).
        """
        if self.begin_date == other_range.begin_date:
            return True
        if self.begin_date < other_range.begin_date:
            # Ok, our time range starts before the other one.
            # In case we have no end date ourselves, we clearly
            # have an overlap.
            if self.end_date is None:
                return True
            # We also have an overlap if our end_date is after
            # the begin_date of the other range.
            if self.end_date > other_range.begin_date:
                return True
        else:
            # Here, we now can be sure that the other range is the one
            # starting earlier.
            if other_range.end_date is None:
                # If that has no defined end date, we can be sure we have an
                # overlap.
                return True
            if other_range.end_date > self.begin_date:
                # Otherwise, we check if the other range ends before our own
                # one starts. If so, we have an overlap.
                return True

        return False

    def covers(self, other_range):
        """Return true if the first range covers the other range completely."""
        if self.begin_date <= other_range.begin_date:
            if self.end_date is None:
                return True
            if other_range.end_date is None:
                return False
            return self.end_date >= other_range.end_date
        return False

    def __contains__(self, other_range):
        """Use the covers method for the contains tests."""
        return self.covers(other_range)
