from project.api.models import ConfigurationDevice
from project.api.models import Platform, Device, ConfigurationPlatform
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.models.test_configurations_model import generate_configuration_model


class TestConfigurationObjectsModel(BaseTestCase):
    """Tests for the ConfigurationDevice & ConfigurationPlatform Models."""

    def test_add_configuration_device_model(self):
        """""Ensure Add configuration device model """
        p = Platform(short_name="Platform 33")
        d = Device(short_name="Device 44")
        conf = generate_configuration_model()
        cd = ConfigurationDevice(calibration_date=fake.date(),
                                 parent_platform=p,
                                 offset_x=fake.coordinate(),
                                 offset_y=fake.coordinate(),
                                 offset_z=fake.coordinate(),
                                 configuration=conf,
                                 device=d,
                                 firmware_version="0.3"
                                 )
        db.session.add_all([p, d, cd])
        db.session.commit()
        self.assertTrue(cd.id is not None)


def test_add_configuration_platform_model(self):
    """""Ensure Add configuration platform model """
    p1 = Platform(short_name="Platform 133")
    p2 = Device(short_name="Platform 233")
    conf = generate_configuration_model()
    cp = ConfigurationPlatform(calibration_date=fake.date(),
                               parent_platform=p1,
                               offset_x=fake.coordinate(),
                               offset_y=fake.coordinate(),
                               offset_z=fake.coordinate(),
                               configuration=conf,
                               platform=p2,
                               firmware_version="0.3"
                               )
    db.session.add_all([p1, p2, cp])
    db.session.commit()
    self.assertTrue(cp.id is not None)
