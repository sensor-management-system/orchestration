"""Roles for the permission groups."""

import enum


class PermissionGroupRole(enum.Enum):
    """
    Options for permission group tests.

    Basically we have 2 roles for the IDL:
    - Member
    - Admin

    Any is a helper so that we can specify that we want to use
    of the roles.
    """

    ANY = 1
    MEMBER = 2
    ADMIN = 3
