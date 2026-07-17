# SPDX-FileCopyrightText: 2026
# - Rubankumar Moorthy <r.moorthy@fz-juelich.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Research Centre Juelich GmbH - Institute of Bio- and Geosciences Agrosphere (IBG-3,
#   https://www.fz-juelich.de/en/ibg/ibg-3)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Marshmallow field for sorted keyword lists."""

from marshmallow import ValidationError
from marshmallow_jsonapi import fields


class SortedStringListField(fields.Field):
    """Serialize and deserialize string lists in case-insensitive order."""

    @staticmethod
    def _sort(values):
        """Sort strings case-insensitively while preserving their spelling."""
        if values is None:
            return None
        return sorted(values, key=lambda value: value.casefold())

    def _serialize(self, value, attr, obj, **kwargs):
        """Return a string list in a stable order."""
        return self._sort(value)

    def _deserialize(self, value, attr, data, **kwargs):
        """Validate and return the incoming string list in a stable order."""
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValidationError("Not a valid list.")
        if any(not isinstance(item, str) for item in value):
            raise ValidationError("List items must be strings.")
        return self._sort(value)
