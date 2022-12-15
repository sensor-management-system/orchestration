"""Wkt field for polygons."""

import shapely.wkt
from geoalchemy2.shape import from_shape
from marshmallow import ValidationError
from marshmallow_jsonapi import fields
from shapely.errors import WKTReadingError

from ...helpers.geometry import geometry_to_wkt


class WktPolygonField(fields.Field):
    """Field to represent polygon fields as well known text."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Transform the geometry value to wkt."""
        return geometry_to_wkt(value)

    def _deserialize(self, value, attr, data, **kwargs):
        """Create the geometry from the wkt value."""
        if value is None:
            return None
        try:
            shape = shapely.wkt.loads(value)
            if shape.geom_type != "Polygon":
                raise ValidationError("Geometry must be a polygon")
            if not shape.is_valid:
                raise ValidationError("Geometry must be valid wkt representation")
            return from_shape(shape)
        except WKTReadingError:
            raise ValidationError("Geometry must be valid wkt representation")
