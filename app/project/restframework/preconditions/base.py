"""Base classes for precondition."""


class Precondition:
    """Class to combine multiple preconditions."""

    def __init__(self, object_rule):
        """Init the object."""
        self.object_rule = object_rule

    def __and__(self, other):
        """Construct a combination of both preconditions."""

        def updated_object_rule(object):
            """Check both preconditions."""
            # In order to ensure both rules are checked
            # we need to use or - as everyone for itself returns None
            # if the precondition is fulfilled.
            # It will return the first error that is found.
            return self.object_rule(object) or other.object_rule(object)

        return Precondition(updated_object_rule)

    def violated_by_object(self, object):
        """
        Return an instance of conflict error if there is a problem.

        Return None, if no violation happens.
        """
        return self.object_rule(object)
