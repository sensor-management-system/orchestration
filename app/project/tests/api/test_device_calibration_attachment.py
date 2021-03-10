import json

from project.api.models import (
    Contact,
    Device,
    DeviceAttachment,
    DeviceCalibrationAction,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_device_calibration_attachment_model import (
    add_device_calibration_attachment,
)

from project import base_url


class TestDeviceCalibrationAttachment(BaseTestCase):
    """Tests for the DeviceCalibrationAttachment endpoints."""

    device_calibration_attachment_url = base_url + "/device-calibration-attachments"
    object_type = "device_calibration_attachment"

    def test_get_generic_device_action_attachment(self):
        """Ensure the GET /device_calibration_attachment route reachable."""
        response = self.client.get(self.device_calibration_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_attachment_collection(self):
        """Test retrieve a collection of DeviceCalibrationAttachment objects"""
        _ = add_device_calibration_attachment()
        with self.client:
            response = self.client.get(self.device_calibration_attachment_url)
        _ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_post_generic_device_action_attachment(self):
        """Create DeviceCalibrationAttachment"""
        # d = Device(short_name="Device 1")
        # jwt1 = generate_token_data()
        # c = Contact(
        #     given_name=jwt1["given_name"],
        #     family_name=jwt1["family_name"],
        #     email=jwt1["email"],
        # )
        # db.session.add(d)
        # db.session.commit()
        # a = DeviceAttachment(label=fake.pystr(), url=fake.url(), device_id=d.id)
        # dca = DeviceCalibrationAction(
        #     description="Test ConfigurationDevice",
        #     current_calibration_date=fake.date(),
        #     next_calibration_date=fake.date(),
        #     device=d,
        #     contact=c,
        # )
        # db.session.add_all([d, a, c, dca])
        # db.session.commit()
        # data = {
        #     "data": {
        #         "type": self.object_type,
        #         "attributes": {},
        #         "relationships": {
        #             "action": {"data": {"type": "action", "id": dca.id}},
        #             "attachment": {"data": {"type": "attachment", "id": a.id}}, },
        #     }
        # }
        # _ = super().add_object(
        #     url=f"{self.device_software_update_action_attachment_url}?include=action,attachment",
        #     data_object=data,
        #     object_type=self.object_type,
        # )

    def test_update_generic_device_action_attachment(self):
        """Update DeviceCalibrationAttachment"""

    def test_delete_generic_device_action_attachment(self):
        """Delete DeviceCalibrationAttachment"""
        dca = add_device_calibration_attachment()
        _ = super().delete_object(
            url=f"{self.device_calibration_attachment_url}/{dca.id}",
        )
