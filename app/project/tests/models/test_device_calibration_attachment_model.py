from project.api.models import (Contact, DeviceCalibrationAction, Device,
                                DeviceCalibrationAttachment,
                                DeviceAttachment)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_token_data


class TestDeviceCalibrationAttachmentModel(BaseTestCase):
    """Tests for the DeviceCalibrationAttachment Models."""

    def test_device_calibration_attachment(self):
        """""Ensure Add DeviceCalibrationAttachment  model."""
        d = Device(short_name="Device 1")
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

        dca = DeviceCalibrationAction(
            description="Test ConfigurationDevice",
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            device=d,
            contact=c,
        )
        dca_a = DeviceCalibrationAttachment(action=dca,
                                            attachment=a)
        db.session.add_all([d, a, c, dca, dca_a])
        db.session.commit()
        self.assertTrue(dca_a.id is not None)
