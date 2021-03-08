from project.api.models import (Device, Contact, DeviceSoftwareUpdateAction,
                                Platform, PlatformSoftwareUpdateAction)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import generate_token_data

from project.tests.base import fake


class TestDeviceSoftwareUpdateActionModel(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateAction Model."""

    def test_add_device_software_update_action_model(self):
        """""Ensure Add DeviceSoftwareUpdateAction model."""
        d = Device(short_name="Device 1")
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        dsu = DeviceSoftwareUpdateAction(
            device=d,
            software_type_name=fake.pystr(),
            software_type_uri=fake.uri(),
            update_date=fake.date(),
            version="0.54",
            repository_url=fake.url(),
            description=fake.paragraph(nb_sentences=3),
            contact=c,

        )
        db.session.add_all([d, c, dsu])
        db.session.commit()
        self.assertTrue(dsu.id is not None)

    def test_add_platform_software_update_action_model(self):
        """""Ensure Add PlatformSoftwareUpdateAction model."""
        p = Platform(short_name="Platform 1")
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        psu = PlatformSoftwareUpdateAction(
            platform=p,
            software_type_name=fake.pystr(),
            software_type_uri=fake.uri(),
            update_date=fake.date(),
            version="0.54",
            repository_url=fake.url(),
            description=fake.paragraph(nb_sentences=3),
            contact=c,

        )
        db.session.add_all([p, c, psu])
        db.session.commit()
        self.assertTrue(psu.id is not None)
