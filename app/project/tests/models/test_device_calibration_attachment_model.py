from project.api.models import (
    Contact,
    Device,
    DeviceAttachment,
    DeviceCalibrationAction,
    DeviceCalibrationAttachment,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data


def add_device_calibration_attachment():
    d = Device(short_name="Device 1")
    mock_jwt = generate_token_data()
    c = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    db.session.add(d)
    db.session.commit()
    a = DeviceAttachment(label=fake.pystr(), url=fake.url(), device_id=d.id)
    dca = DeviceCalibrationAction(
        description="Test ConfigurationDevice",
        current_calibration_date=fake.date(),
        next_calibration_date=fake.date(),
        device=d,
        contact=c,
    )
    dca_a = DeviceCalibrationAttachment(action=dca, attachment=a)
    db.session.add_all([d, a, c, dca, dca_a])
    db.session.commit()
    return dca_a


class TestDeviceCalibrationAttachmentModel(BaseTestCase):
    """Tests for the DeviceCalibrationAttachment Models."""

    def test_device_calibration_attachment(self):
        """""Ensure Add DeviceCalibrationAttachment  model."""
        dca_a = add_device_calibration_attachment()
        self.assertTrue(dca_a.id is not None)
