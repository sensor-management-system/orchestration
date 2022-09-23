"""Some dsl like classes to construct complex permission objects."""

from flask import g

from ...extensions.idl.roles import PermissionGroupRole
from ...extensions.instances import idl
from .base import ObjectRestriction, Permissions


class RequireUserForRequest(Permissions):
    """Requires a user."""

    def __init__(self):
        """Init the object."""
        super().__init__(lambda: g.user is not None, lambda _: True)


class RestrictObjectTo(Permissions):
    """Restricts the object permission accoding to more granular rules."""

    def __init__(self, object_restriction):
        """Init the object."""

        def always_true():
            return True

        super().__init__(always_true, object_restriction.object_rule)


class SuperUser(ObjectRestriction):
    """Require a super user for the object permission."""

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Require a super user."""
            return g.user and g.user.is_superuser

        super().__init__(object_rule)


class OwnerOfPrivateEntity(ObjectRestriction):
    """Require that the owner (created_by_id) of a private entity is the current user."""

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Check if the current user is the owner and that the object is private."""
            return g.user and object.is_private and object.created_by_id == g.user.id

        super().__init__(object_rule)


class NoPrivateEntity(ObjectRestriction):
    """
    Don't allow object permission for private objects.

    This is more a restriction to compose with others.
    For example: If we don't want to query the idl for private objects.
    """

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return true if the object is not private."""
            return not object.is_private

        super().__init__(object_rule)


class GetPermissionGroupsFromDeviceOrPlatform:
    """Helper class to get the permission groups of a device or a platform."""

    def __call__(self, model):
        """Return the permission groups of the device or platform."""
        return model.group_ids


class GetPermissionGroupForConfiguration:
    """
    Helper class to get the permission group of a platform.

    Will return a list, in order to be compatible with
    GetPermissionGroupsFromDeviceOrPlatform.
    """

    def __call__(self, model):
        """Return a list with the single permission group."""
        return [model.cfg_permission_group]


class RoleInPermissionGroup(ObjectRestriction):
    """
    Restrict object permissions to a user with a certain role in one permission group.

    We can use any here of PermissionGroupRole - including the 'ANY' entry
    if we don't care about the specific role.
    """

    def __init__(self, permission_group_role, extract_permission_groups):
        """Init the object."""

        def object_rule(model):
            """Check for the permission groups."""
            if not g.user:
                return False
            if not hasattr(g, "idl_user"):
                g.idl_user = idl.get_all_permission_groups_for_a_user(g.user.subject)
            if not g.idl_user:
                return False
            checked_fields = []
            if permission_group_role in [
                PermissionGroupRole.ADMIN,
                PermissionGroupRole.ANY,
            ]:
                checked_fields.extend(g.idl_user.administrated_permission_groups)
            if permission_group_role in [
                PermissionGroupRole.MEMBER,
                PermissionGroupRole.ANY,
            ]:
                checked_fields.extend(g.idl_user.membered_permission_groups)
            if not any(x in extract_permission_groups(model) for x in checked_fields):
                return False
            return True

        super().__init__(object_rule)
