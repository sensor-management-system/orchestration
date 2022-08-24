"""Tests for the device software update action api."""

import json

from project import base_url
from project.api.models import Contact, Device, DeviceSoftwareUpdateAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.models.test_software_update_actions_model import (
    add_device_software_update_action_model,
)


class TestDeviceSoftwareUpdateAction(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateAction endpoints."""

    url = base_url + "/device-software-update-actions"
    object_type = "device_software_update_action"

    def test_get_device_software_update_action(self):
        """Ensure the GET /device_software_update_action route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_software_update_action_collection(self):
        """Test retrieve a collection of DeviceSoftwareUpdateAction objects."""
        sau = add_device_software_update_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sau.description, data["data"][0]["attributes"]["description"])

    def test_post_device_software_update_action(self):
        """Create DeviceSoftwareUpdateAction."""
        userinfo = generate_userinfo_data()
        device = Device(
            short_name="Device 1",
            is_public=False,
            is_private=False,
            is_internal=True,
        )

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
                    "version": f"v_{fake.pyint()}",
                    "software_type_name": fake.pystr(),
                    "software_type_uri": fake.uri(),
                    "repository_url": fake.url(),
                    "update_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        result = super().add_object(
            url=f"{self.url}?include=device,contact",
            data_object=data,
            object_type=self.object_type,
        )
        device_id = result["data"]["relationships"]["device"]["data"]["id"]
        device = db.session.query(Device).filter_by(id=device_id).first()
        self.assertEqual(device.update_description, "create;software update action")

    def test_update_device_software_update_action(self):
        """Update DeviceSoftwareUpdateAction."""
        device_software_update_action = add_device_software_update_action_model()
        device_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        result = super().update_object(
            url=f"{self.url}/{device_software_update_action.id}",
            data_object=device_software_update_action_updated,
            object_type=self.object_type,
        )
        device_id = result["data"]["relationships"]["device"]["data"]["id"]
        device = db.session.query(Device).filter_by(id=device_id).first()
        self.assertEqual(device.update_description, "update;software update action")

    def test_delete_device_software_update_action(self):
        """Delete DeviceSoftwareUpdateAction."""
        device_software_update_action = add_device_software_update_action_model()
        device_id = device_software_update_action.device_id
        _ = super().delete_object(
            url=f"{self.url}/{device_software_update_action.id}",
        )
        device = db.session.query(Device).filter_by(id=device_id).first()
        self.assertEqual(device.update_description, "delete;software update action")

    def test_filtered_by_device(self):
        """Ensure that I can prefilter by a specific devices."""
        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        device1 = Device(
            short_name="device1",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceSoftwareUpdateAction(
            contact=contact,
            device=device1,
            description="Some first action",
            software_type_name="firmware",
            update_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceSoftwareUpdateAction(
            contact=contact,
            device=device2,
            description="Some other action",
            software_type_name="sampleScript",
            update_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/device-software-update-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # test only for the first device
        with self.client:
            url_get_for_device1 = (
                base_url + f"/devices/{device1.id}/device-software-update-actions"
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
                base_url + f"/devices/{device2.id}/device-software-update-actions"
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
                base_url
                + f"/devices/{device2.id + 9999}/device-software-update-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_device,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
