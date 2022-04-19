from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.tests.base import BaseTestCase


def generate_configuration_model():
    platform1 = Platform(short_name="Platform 1",
                         is_public=False,
                         is_private=False,
                         is_internal=True,
                         )
    platform2 = Platform(short_name="Platform 2",
                         is_public=False,
                         is_private=False,
                         is_internal=True,
                         )
    platform3 = Platform(short_name="Platform 3",
                         is_public=False,
                         is_private=False,
                         is_internal=True,
                         )
    db.session.add(platform1)
    db.session.add(platform2)
    db.session.add(platform3)
    device1 = Device(short_name="Device 1",
                     is_public=False,
                     is_private=False,
                     is_internal=True,
                     )
    device2 = Device(short_name="Device 2",
                     is_public=False,
                     is_private=False,
                     is_internal=True,
                     )
    device3 = Device(short_name="Device 3",
                     is_public=False,
                     is_private=False,
                     is_internal=True,
                     )
    db.session.add(device1)
    db.session.add(device2)
    db.session.add(device3)
    config1 = Configuration(label="Config1", location_type="static",
                            is_public=False,
                            is_internal=True,
                            )
    db.session.add(config1)
    db.session.commit()
    db.session.commit()
    return config1


class TestConfigurationsModel(BaseTestCase):
    """Tests for the Configurations Model."""

    def test_add_configuration_model(self):
        """""Ensure Add Configuration model """

        generate_configuration_model()

        c = db.session.query(Configuration).filter_by(label="Config1").first()
        self.assertEqual("static", c.location_type)
