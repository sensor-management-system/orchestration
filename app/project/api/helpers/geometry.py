"""Geometry related helper functions."""

from geoalchemy2.shape import to_shape


def geometry_to_wkt(value):
    """Transform a geometry to WKT."""
    if value is None:
        return None
    shape = to_shape(value)
    return shape.wkt
