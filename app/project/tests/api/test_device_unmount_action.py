"""Tests for the device unmount actions api."""

import json

from project import base_url
from project.api.models import Configuration, Contact, Device, DeviceUnmountAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_unmount_actions_model import add_unmount_device_action


class TestDeviceUnmountAction(BaseTestCase):
    """Tests for the DeviceUnmountAction endpoints."""

    url = base_url + "/device-unmount-actions"
    object_type = "device_unmount_action"

    def test_get_device_unmount_action(self):
        """Ensure the GET /device_unmount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_unmount_action_collection(self):
        """Test retrieve a collection of DeviceUnmountAction objects."""
        unmount_device_action = add_unmount_device_action()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            unmount_device_action.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            data["data"][0]["attributes"]["end_date"],
        )

    def test_post_device_unmount_action(self):
        """Create DeviceUnmountAction."""
        device = Device(
            short_name=fake.linux_processor(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = generate_configuration_model()
        db.session.add_all([device, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "test unmount device action",
                    "end_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device,contact,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_unmount_action(self):
        """Update DeviceUnmountAction."""
        unmount_device_action = add_unmount_device_action()
        unmount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": unmount_device_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{unmount_device_action.id}",
            data_object=unmount_device_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_unmount_action(self):
        """Delete DeviceUnmountAction."""
        unmount_device_action = add_unmount_device_action()
        _ = super().delete_object(
            url=f"{self.url}/{unmount_device_action.id}",
        )

    def test_filtered_by_configuration(self):
        """Ensure that I can prefilter by a specific configuration."""
        configuration1 = Configuration(
            label="sample configuration", location_type="static",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II", location_type="static",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        device1 = Device(short_name="device1",
                         is_public=False,
                         is_private=False,
                         is_internal=True,
                         )
        db.session.add(device1)

        device2 = Device(short_name="device2",
                         is_public=False,
                         is_private=False,
                         is_internal=True,
                         )
        db.session.add(device2)

        action1 = DeviceUnmountAction(
            configuration=configuration1,
            contact=contact,
            device=device1,
            description="Some first action",
            end_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceUnmountAction(
            configuration=configuration2,
            contact=contact,
            device=device2,
            description="Some other action",
            end_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/device-unmount-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first configuration
        with self.client:
            url_get_for_configuration1 = (
                    base_url + f"/configurations/{configuration1.id}/device-unmount-actions"
            )
            response = self.client.get(
                url_get_for_configuration1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second configuration
        with self.client:
            url_get_for_configuration2 = (
                    base_url + f"/configurations/{configuration2.id}/device-unmount-actions"
            )
            response = self.client.get(
                url_get_for_configuration2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_configuration = (
                    base_url
                    + f"/configurations/{configuration2.id + 9999}/device-unmount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_configuration,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_device(self):
        """Ensure that I can prefilter by a specific devices."""
        configuration1 = Configuration(
            label="sample configuration", location_type="static",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II", location_type="static",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        device1 = Device(short_name="device1",
                         is_public=False,
                         is_private=False,
                         is_internal=True,
                         )
        db.session.add(device1)

        device2 = Device(short_name="device2",
                         is_public=False,
                         is_private=False,
                         is_internal=True,
                         )
        db.session.add(device2)

        action1 = DeviceUnmountAction(
            configuration=configuration1,
            contact=contact,
            device=device1,
            description="Some first action",
            end_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceUnmountAction(
            configuration=configuration2,
            contact=contact,
            device=device2,
            description="Some other action",
            end_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first device
        with self.client:
            url_get_for_device1 = (
                    base_url + f"/devices/{device1.id}/device-unmount-actions"
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
                    base_url + f"/devices/{device2.id}/device-unmount-actions"
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
                    base_url + f"/devices/{device2.id + 9999}/device-unmount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_device,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)
