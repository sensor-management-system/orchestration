from project.api.models import User, Contact
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.tests.base import BaseTestCase
from project.tests.base import fake, generate_userinfo_data


def generate_configuration_model(
    is_public=False, is_private=False, is_internal=True,
):
    userinfo = generate_userinfo_data()
    device = Device(
        short_name=fake.linux_processor(),
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    device_parent_platform = Platform(
        short_name="device parent platform",
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    platform = Platform(
        short_name=fake.linux_processor(),
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    parent_platform = Platform(
        short_name="platform parent-platform",
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    configuration = Configuration(
        label=fake.linux_processor(),
        is_public=is_public,
        is_internal=is_internal,
    )
    db.session.add_all(
        [
            device,
            device_parent_platform,
            platform,
            parent_platform,
            contact,
            configuration,
        ]
    )
    db.session.commit()
    return configuration


class TestConfigurationsModel(BaseTestCase):
    """Tests for the Configurations Model."""

    def test_add_configuration_model(self):
        """""Ensure Add Configuration model """

        generate_configuration_model()

        c = db.session.query(Configuration).filter_by(label="Config1").first()
        self.assertEqual("static", c.location_type)
