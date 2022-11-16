"""Test classes for the wkt polygon field."""

from argparse import Namespace

import shapely.wkt
from geoalchemy2.shape import from_shape
from marshmallow import ValidationError

from project.api.serializer.fields.wkt_polygon_field import WktPolygonField
from project.tests.base import BaseTestCase


class TestWktPolygonField(BaseTestCase):
    """Tests for the WktPolygonField."""

    def setUp(self):
        """Set up the data for the tests."""
        super().setUp()
        self.field = WktPolygonField()

    def test_deserialize_ok(self):
        """Ensure we deserialize wkt to a geometry."""
        wkt_value = "POLYGON ((10 10, 10 20, 20 20, 20 10, 10 10))"
        self.field.deserialize(wkt_value)

    def test_deserialize_no_polygon(self):
        """Ensure we don't accept points - but require polygons."""
        wkt_value = "POINT (10 10)"
        with self.assertRaises(ValidationError):
            self.field.deserialize(wkt_value)

    def test_deserialize_no_valid_wkt(self):
        """Ensure we raise an Exception if we don't get valid wkt."""
        wkt_values = [
            "POLYGON ((10 10 10, 20, 20 20, 20 10, 10 10))",
            "bla",
        ]
        for wkt_value in wkt_values:
            with self.assertRaises(ValidationError):
                self.field.deserialize(wkt_value)

    def test_serialize_ok(self):
        """Ensure the serialization with a Geometry works."""
        wkt_value = "POLYGON ((10 10, 10 20, 20 20, 20 10, 10 10))"
        shape = shapely.wkt.loads(wkt_value)
        geom = from_shape(shape)

        fake_model = Namespace(field=geom)
        serialized_value = self.field.serialize("field", fake_model)
        self.assertEqual(serialized_value, wkt_value)

    def test_serialize_none(self):
        """Ensure we return None if we try to serialize None."""
        fake_model = Namespace(field=None)
        serialized_value = self.field.serialize("field", fake_model)
        self.assertIsNone(serialized_value)
