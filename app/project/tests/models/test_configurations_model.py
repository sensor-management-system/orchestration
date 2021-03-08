import unittest

from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.configuration_device import ConfigurationDevice
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.tests.base import BaseTestCase


def generate_configuration_model():
    platform1 = Platform(short_name="Platform 1")
    platform2 = Platform(short_name="Platform 2")
    platform3 = Platform(short_name="Platform 3")
    db.session.add(platform1)
    db.session.add(platform2)
    db.session.add(platform3)
    device1 = Device(short_name="Device 1")
    device2 = Device(short_name="Device 2")
    device3 = Device(short_name="Device 3")
    db.session.add(device1)
    db.session.add(device2)
    db.session.add(device3)
    config1 = Configuration(label="Config1", location_type="static")
    db.session.add(config1)
    db.session.commit()
    platform1_conf = ConfigurationPlatform(
        platform=platform1,
        configuration=config1,
        offset_x=1.0,
        offset_y=1.0,
        offset_z=1.0,
    )
    db.session.add(platform1_conf)
    platform2_conf = ConfigurationPlatform(
        platform=platform2,
        configuration=config1,
        parent_platform=platform1,
        offset_x=2.0,
        offset_y=2.0,
        offset_z=2.0,
    )
    platform3_conf = ConfigurationPlatform(
        platform=platform3,
        configuration=config1,
        offset_x=13.5,
        offset_y=13.5,
        offset_z=13.5,
    )
    db.session.add(platform2_conf)
    db.session.add(platform3_conf)
    device1_conf = ConfigurationDevice(
        device=device1,
        configuration=config1,
        parent_platform=platform2,
        offset_x=0.5,
        offset_y=0.5,
        offset_z=0.5,
    )
    device2_conf = ConfigurationDevice(
        device=device2,
        configuration=config1,
        parent_platform=platform2,
        offset_x=0.6,
        offset_y=0.6,
        offset_z=0.6,
    )
    device3_conf = ConfigurationDevice(
        device=device3,
        configuration=config1,
        parent_platform=platform2,
        offset_x=0.65,
        offset_y=0.65,
        offset_z=0.65,
    )
    db.session.add(device1_conf)
    db.session.add(device2_conf)
    db.session.add(device3_conf)
    db.session.commit()
    return config1


class TestConfigurationsModel(BaseTestCase):
    """Tests for the Configurations Model."""

    def test_add_configuration_model(self):
        """""Ensure Add Configuration model """

        generate_configuration_model()

        c = db.session.query(Configuration).filter_by(label="Config1").first()
        self.assertEqual("static", c.location_type)


if __name__ == "__main__":
    unittest.main()
