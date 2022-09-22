"""Some base classes for permissions."""


class Permissions:
    """Base class to combine permission checks."""

    def __init__(self, request_rule, object_rule):
        """Init the object."""
        self.request_rule = request_rule
        self.object_rule = object_rule

    def __and__(self, other):
        """Restrict the access to fulfill both checks."""

        def updated_request_rule():
            """Run both checks combined."""
            return self.request_rule() and other.request_rule()

        def updated_object_rule(object):
            """Run both checks for the object."""
            return other.object_rule(object) and self.object_rule(object)

        return Permissions(updated_request_rule, updated_object_rule)

    def has_permission(self):
        """Return true if the permission for the request is given."""
        return self.request_rule()

    def has_object_permission(self, object):
        """Return true if the request for the object is give."""
        return self.object_rule(object)


class ObjectRestriction:
    """Helper class to just combine the restrictions for the object permission."""

    def __init__(self, object_rule):
        """Init the object."""
        self.object_rule = object_rule

    def __or__(self, other):
        """Construct a restriction that will enforce one of the conditions."""

        def updated_object_rule(object):
            """Return true of one of the conditions are fulfilled."""
            return self.object_rule(object) or other.object_rule(object)

        return ObjectRestriction(updated_object_rule)

    def __and__(self, other):
        """Construct a restriction that will enforce both of the conditions."""

        def updated_object_rule(object):
            """Return true if both of the conditions are fulfilled."""
            return self.object_rule(object) and other.object_rule(object)

        return ObjectRestriction(updated_object_rule)
