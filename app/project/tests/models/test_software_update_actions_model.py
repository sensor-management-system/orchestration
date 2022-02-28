from project.api.models import (
    Contact,
    Device,
    DeviceSoftwareUpdateAction,
    Platform,
    PlatformSoftwareUpdateAction,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def add_device_software_update_action_model():
    userinfo = generate_userinfo_data()
    d = Device(
        short_name="Device 1", is_public=False, is_private=False, is_internal=True,
    )

    c = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    device_software_update_action = DeviceSoftwareUpdateAction(
        device=d,
        software_type_name=fake.pystr(),
        software_type_uri=fake.uri(),
        update_date=fake.date(),
        version="0.54",
        repository_url=fake.url(),
        description=fake.paragraph(nb_sentences=3),
        contact=c,
    )
    db.session.add_all([d, c, device_software_update_action])
    db.session.commit()
    return device_software_update_action


def add_platform_software_update_action_model():
    userinfo = generate_userinfo_data()
    p = Platform(
        short_name="Platform 1", is_public=False, is_private=False, is_internal=True,
    )

    c = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    platform_software_update_action = PlatformSoftwareUpdateAction(
        platform=p,
        software_type_name=fake.pystr(),
        software_type_uri=fake.uri(),
        update_date=fake.date(),
        version="0.54",
        repository_url=fake.url(),
        description=fake.paragraph(nb_sentences=3),
        contact=c,
    )
    db.session.add_all([p, c, platform_software_update_action])
    db.session.commit()
    return platform_software_update_action


class TestDeviceSoftwareUpdateActionModel(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateAction Model."""

    def test_add_device_software_update_action_model(self):
        """""Ensure Add DeviceSoftwareUpdateAction model."""
        device_software_update_action = add_device_software_update_action_model()
        self.assertTrue(device_software_update_action.id is not None)

    def test_add_platform_software_update_action_model(self):
        """""Ensure Add PlatformSoftwareUpdateAction model."""
        platform_software_update_action = add_platform_software_update_action_model()
        self.assertTrue(platform_software_update_action.id is not None)
