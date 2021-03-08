from project.api.models import (Platform, Contact, DeviceAttachment,
                                DeviceSoftwareUpdateActionAttachment,
                                DeviceSoftwareUpdateAction,
                                PlatformSoftwareUpdateActionAttachment,
                                PlatformSoftwareUpdateAction, Device, PlatformAttachment)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import generate_token_data, fake


def add_device_software_update_action_attachment():
    d = Device(short_name="Device 133")
    jwt1 = generate_token_data()
    c = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )
    db.session.add(d)
    db.session.commit()
    a = DeviceAttachment(label=fake.pystr(),
                         url=fake.url(),
                         device_id=d.id)
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
    dca_a = DeviceSoftwareUpdateActionAttachment(action=dsu,
                                                 attachment=a)
    db.session.add_all([d, a, c, dsu, dca_a])
    db.session.commit()
    return dca_a


class TestSoftwareUpdateActionAttachmentModel(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateActionAttachment &
    PlatformSoftwareUpdateActionAttachment Models."""

    def test_device_software_update_action_attachment_model(self):
        """""Ensure Add DeviceSoftwareUpdateActionAttachment  model."""
        dca_a = add_device_software_update_action_attachment()
        self.assertTrue(dca_a.id is not None)

    def test_platform_software_update_action_attachment_model(self):
        """""Ensure Add PlatformSoftwareUpdateActionAttachment  model."""
        p = Platform(short_name="Platform 144")
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        db.session.add(p)
        db.session.commit()
        a = PlatformAttachment(label=fake.pystr(),
                               url=fake.url(),
                               platform_id=p.id)

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
        dca_a = PlatformSoftwareUpdateActionAttachment(action=psu,
                                                       attachment=a)
        db.session.add_all([p, a, c, psu, dca_a])
        db.session.commit()
        self.assertTrue(dca_a.id is not None)
