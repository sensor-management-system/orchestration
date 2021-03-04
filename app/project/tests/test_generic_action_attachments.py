from project.api.models.base_model import db
from project.api.models.device_attachment import DeviceAttachment
from project.api.models.generic_action_attachments import (
    GenericDeviceActionAttachment,
    GenericPlatformActionAttachment,
)
from project.api.models.platform_attachment import PlatformAttachment
from project.tests.base import BaseTestCase, fake
from project.tests.test_generic_actions_models import (
    generate_device_action_model,
    generate_platform_action_model,
)


class TestGenericActions(BaseTestCase):
    """
    Test Generic Actions
    """

    def test_add_generic_platform_action_attachment_model(self):
        """""Ensure Add generic platform action attachment model """
        gpa = generate_platform_action_model()
        a1 = PlatformAttachment(
            label="platform attachment1",
            url=fake.image_url(),
            platform_id=gpa.platform_id,
        )

        a2 = PlatformAttachment(
            label="platform attachment2",
            url=fake.image_url(),
            platform_id=gpa.platform_id,
        )
        gpa_attachment = GenericPlatformActionAttachment()
        gpa_attachment.action = gpa
        gpa_attachment.attachment = a1
        gpa_attachment.attachment = a2
        db.session.add_all([a1, a2, gpa_attachment])
        db.session.commit()
        gpa_t = (
            db.session.query(GenericPlatformActionAttachment)
            .filter_by(action_id=gpa.id)
            .one()
        )
        self.assertEqual("test GenericPlatformAction", gpa_t.action.description)

    def test_add_generic_device_action_attachment_model(self):
        """""Ensure Add generic device action attachment model """
        gpa = generate_device_action_model()
        a1 = DeviceAttachment(
            label="device attachment1", url=fake.image_url(), device_id=gpa.device_id
        )
        a2 = DeviceAttachment(
            label="device attachment2", url=fake.image_url(), device_id=gpa.device_id
        )
        gpa_attachment = GenericDeviceActionAttachment()
        gpa_attachment.action = gpa
        gpa_attachment.attachment = a1
        gpa_attachment.attachment = a2
        db.session.add_all([a1, a2, gpa_attachment])
        db.session.commit()
        gpa_t = (
            db.session.query(GenericDeviceActionAttachment)
            .filter_by(action_id=gpa.id)
            .one()
        )
        self.assertEqual("test GenericDeviceAction", gpa_t.action.description)
