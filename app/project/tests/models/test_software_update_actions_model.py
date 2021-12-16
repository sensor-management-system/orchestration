from project.api.models import (
    Contact,
    Device,
    DeviceSoftwareUpdateAction,
    Platform,
    PlatformSoftwareUpdateAction,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data


def add_device_software_update_action_model():
    d = Device(
        short_name="Device 1", is_public=True, is_private=False, is_internal=False,
    )
    mock_jwt = generate_token_data()
    c = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
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
    p = Platform(
        short_name="Platform 1", is_public=True, is_private=False, is_internal=False,
    )
    mock_jwt = generate_token_data()
    c = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
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
