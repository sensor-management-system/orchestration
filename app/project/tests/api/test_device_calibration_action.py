"""Tests for the device calibration api."""

import json

from project import base_url
from project.api.models import Contact, Device, DeviceCalibrationAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.models.test_device_calibration_action_model import (
    add_device_calibration_action,
)
from project.tests.models.test_device_calibration_action_model import (
    add_device_property_calibration_model,
)
from project.tests.models.test_device_calibration_attachment_model import (
    add_device_calibration_attachment,
)


class TestDeviceCalibrationAction(BaseTestCase):
    """Tests for the DeviceCalibrationAction endpoints."""

    url = base_url + "/device-calibration-actions"
    object_type = "device_calibration_action"

    def test_get_device_calibration_action(self):
        """Ensure the GET /device_calibration_action route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of DeviceCalibrationAction objects."""
        device_calibration_action = add_device_calibration_action()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            device_calibration_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_device_calibration_action(self):
        """Create DeviceCalibrationAction."""
        device = Device(short_name="Device 12")
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all([device, contact])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test DeviceCalibrationAction",
                    "formula": fake.pystr(),
                    "value": fake.pyfloat(),
                    "current_calibration_date": fake.future_datetime().__str__(),
                    "next_calibration_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_calibration_action(self):
        """Update DeviceCalibration."""
        device_calibration_action = add_device_calibration_action()
        device_calibration_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_calibration_action.id,
                "attributes": {"description": "updated",},
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{device_calibration_action.id}",
            data_object=device_calibration_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_calibration_action(self):
        """Delete DeviceCalibrationAction."""
        device_calibration_action = add_device_calibration_action()
        _ = super().delete_object(url=f"{self.url}/{device_calibration_action.id}",)

    def test_filtered_by_device(self):
        """Ensure that I can prefilter by a specific device."""
        device1 = Device(short_name="sample device")
        db.session.add(device1)
        device2 = Device(short_name="sample device II")
        db.session.add(device2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        action1 = DeviceCalibrationAction(
            device=device1,
            contact=contact,
            description="Some first action",
            current_calibration_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceCalibrationAction(
            device=device2,
            contact=contact,
            description="Some other action",
            current_calibration_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/device-calibration-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first device
        with self.client:
            url_get_for_device1 = (
                base_url + f"/devices/{device1.id}/device-calibration-actions"
            )
            response = self.client.get(
                url_get_for_device1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second device
        with self.client:
            url_get_for_device2 = (
                base_url + f"/devices/{device2.id}/device-calibration-actions"
            )
            response = self.client.get(
                url_get_for_device2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url + f"/devices/{device2.id + 9999}/device-calibration-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 404)

    def test_delete_device_calibration_action_with_an_attachment_link(self):
        """Make sure the deletion of a DeviceCalibrationAction can be done even
        if it linked to an attachment."""

        device_calibration_action = add_device_calibration_attachment()
        _ = super().delete_object(url=f"{self.url}/{device_calibration_action.id}",)

    def test_delete_device_caliubration_action_with_device_property_link(self):
        """
        Make sure that the deletion of a DeviceCalibrationAction can be done
        even it it links to an device property.
        """
        device_property_calibration = add_device_property_calibration_model()
        device_calibration_action_id = device_property_calibration.calibration_action_id
        _ = super().delete_object(url=f"{self.url}/{device_calibration_action_id}",)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
