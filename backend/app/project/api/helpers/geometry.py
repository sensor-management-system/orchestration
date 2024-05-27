# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Geometry related helper functions."""

from geoalchemy2.shape import to_shape


def geometry_to_wkt(value):
    """Transform a geometry to WKT."""
    if value is None:
        return None
    shape = to_shape(value)
    return shape.wkt
