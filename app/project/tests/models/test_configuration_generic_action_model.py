from project.api.models import (
    ConfigurationDevice,
    ConfigurationPlatform,
    Device,
    Platform,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake
from project.tests.models.test_configurations_model import generate_configuration_model


class TestConfigurationObjectsModel(BaseTestCase):
    """Tests for the ConfigurationDevice & ConfigurationPlatform Models."""

    def test_add_configuration_device_model(self):
        """""Ensure Add configuration device model """
        parent_platform = Platform(short_name="Platform 33",
                                   is_public=False,
                                   is_private=False,
                                   is_internal=True,
                                   )
        device = Device(short_name="Device 44",
                        is_public=False,
                        is_private=False,
                        is_internal=True,
                        )
        conf = generate_configuration_model()
        cd = ConfigurationDevice(
            parent_platform=parent_platform,
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            configuration=conf,
            device=device,
            firmware_version="0.3",
        )
        db.session.add_all([parent_platform, device, cd])
        db.session.commit()
        self.assertTrue(cd.id is not None)

    def test_add_configuration_platform_model(self):
        """""Ensure Add configuration platform model """
        parent_platform = Platform(short_name="Platform 133",
                                   is_public=False,
                                   is_private=False,
                                   is_internal=True,
                                   )
        platform = Platform(short_name="Platform 233",
                            is_public=False,
                            is_private=False,
                            is_internal=True,
                            )
        conf = generate_configuration_model()
        cp = ConfigurationPlatform(
            parent_platform=parent_platform,
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            configuration=conf,
            platform=platform,
        )
        db.session.add_all([parent_platform, platform, cp])
        db.session.commit()
        self.assertTrue(cp.id is not None)
