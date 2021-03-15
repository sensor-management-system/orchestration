from project import base_url
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.tests.base import BaseTestCase


class TestPlatformModel(BaseTestCase):
    """
    Test Event Services
    """

    def test_add_platform_model(self):
        """""Ensure Add platform model """
        platform = Platform(
            id=13,
            short_name="short_name test",
            description="description test",
            long_name="long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv.de/manufacturer_uri",
            model="model test",
            platform_type_uri="http://cv.de/platform_type_uri",
            platform_type_name="platform_type_name test",
            status_uri="http://cv.de/status_uri test",
            status_name="status_name test",
            website="http://website.de/platform",
            inventory_number="inventory_number test",
            serial_number="serial_number test",
            persistent_identifier="persistent_identifier_test",
        )
        PlatformSchema().dump(platform)
        db.session.add(platform)
        db.session.commit()

        p = db.session.query(Platform).filter_by(id=platform.id).one()
        self.assertIn(p.persistent_identifier, "persistent_identifier_test")
