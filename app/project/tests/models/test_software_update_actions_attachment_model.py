from project.api.models import (
    Contact,
    Device,
    DeviceAttachment,
    DeviceSoftwareUpdateAction,
    DeviceSoftwareUpdateActionAttachment,
    Platform,
    PlatformAttachment,
    PlatformSoftwareUpdateAction,
    PlatformSoftwareUpdateActionAttachment,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def add_device_software_update_action_attachment():
    d = Device(short_name="Device 133")
    userinfo = generate_userinfo_data()
    c = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add(d)
    db.session.commit()
    a = DeviceAttachment(label=fake.pystr(), url=fake.url(), device_id=d.id)
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
    dca_a = DeviceSoftwareUpdateActionAttachment(
        action=device_software_update_action, attachment=a
    )
    db.session.add_all([d, a, c, device_software_update_action, dca_a])
    db.session.commit()
    return dca_a


def add_platform_software_update_action_attachment_model():
    p = Platform(short_name="Platform 144")
    userinfo = generate_userinfo_data()
    c = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add(p)
    db.session.commit()
    a = PlatformAttachment(label=fake.pystr(), url=fake.url(), platform_id=p.id)
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
    dca_a = PlatformSoftwareUpdateActionAttachment(
        action=platform_software_update_action, attachment=a
    )
    db.session.add_all([p, a, c, platform_software_update_action, dca_a])
    db.session.commit()
    return dca_a


class TestSoftwareUpdateActionAttachmentModel(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateActionAttachment &
    PlatformSoftwareUpdateActionAttachment Models."""

    def test_device_software_update_action_attachment_model(self):
        """""Ensure Add DeviceSoftwareUpdateActionAttachment  model."""
        device_software_update_action_attachment = (
            add_device_software_update_action_attachment()
        )
        self.assertTrue(device_software_update_action_attachment.id is not None)

    def test_platform_software_update_action_attachment_model(self):
        """""Ensure Add PlatformSoftwareUpdateActionAttachment  model."""
        platform_software_update_action_attachment = (
            add_platform_software_update_action_attachment_model()
        )
        self.assertTrue(platform_software_update_action_attachment.id is not None)
