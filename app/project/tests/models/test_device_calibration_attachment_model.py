from project.api.models import (
    Contact,
    Device,
    DeviceAttachment,
    DeviceCalibrationAction,
    DeviceCalibrationAttachment,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def add_device_calibration_attachment():
    userinfo = generate_userinfo_data()
    device = Device(short_name="Device 1",
                    is_public=False,
                    is_private=False,
                    is_internal=True,
                    )
    mock_jwt = generate_token_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add(device)
    db.session.commit()
    attachment = DeviceAttachment(
        label=fake.pystr(), url=fake.url(), device_id=device.id
    )
    device_calibration_action = DeviceCalibrationAction(
        description="Test ConfigurationDevice",
        current_calibration_date=fake.date(),
        next_calibration_date=fake.date(),
        device=device,
        contact=contact,
    )
    device_calibration_attachment = DeviceCalibrationAttachment(
        action=device_calibration_action, attachment=attachment
    )
    db.session.add_all(
        [
            device,
            attachment,
            contact,
            device_calibration_action,
            device_calibration_attachment,
        ]
    )
    db.session.commit()
    return device_calibration_attachment


class TestDeviceCalibrationAttachmentModel(BaseTestCase):
    """Tests for the DeviceCalibrationAttachment Models."""

    def test_device_calibration_attachment(self):
        """""Ensure Add DeviceCalibrationAttachment  model."""
        device_calibration_attachment = add_device_calibration_attachment()
        self.assertTrue(device_calibration_attachment.id is not None)
