# SPDX-FileCopyrightText: 2025
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Classes for the permission groups."""

import re

from .base_model import db


class PermissionGroup(db.Model):
    """Model for a permission group."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    entitlement = db.Column(db.String(256), nullable=True, unique=True)

    def __str__(self):
        """Return a string representation of the group."""
        return self.name

    @staticmethod
    def convert_entitlement_to_name(entitlement):
        """Extract the name from the entitlement."""
        pattern = r"^(.+?):(res|group):(?P<name_part>.+)#(.*)$"
        match_result = re.search(pattern, entitlement)
        if match_result:
            return match_result.group("name_part")
        return entitlement
