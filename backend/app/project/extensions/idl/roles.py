# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

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
