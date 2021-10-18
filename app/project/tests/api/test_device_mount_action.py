"""Tests for the device mount action api."""

import json

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    Platform,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_mount_actions_model import add_mount_device_action_model


class TestDeviceMountAction(BaseTestCase):
    """Tests for the DeviceMountAction endpoints."""

    url = base_url + "/device-mount-actions"
    object_type = "device_mount_action"

    def test_get_device_mount_action(self):
        """Ensure the GET /device_mount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_mount_action_collection(self):
        """Test retrieve a collection of DeviceMountAction objects."""
        mount_device_action = add_mount_device_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mount_device_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_device_mount_action(self):
        """Create DeviceMountAction."""
        device = Device(
            short_name=fake.linux_processor(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        parent_platform = Platform(
            short_name="device parent platform",
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
        db.session.add_all([device, parent_platform, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test DeviceMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device,contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_mount_action(self):
        """Update DeviceMountAction."""
        mount_device_action = add_mount_device_action_model()
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{mount_device_action.id}",
            data_object=mount_device_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_mount_action(self):
        """Delete DeviceMountAction."""
        mount_device_action = add_mount_device_action_model()
        _ = super().delete_object(
            url=f"{self.url}/{mount_device_action.id}",
        )

    def test_filtered_by_configuration(self):
        """Ensure that I can prefilter by a specific configuration."""
        configuration1 = Configuration(
            label="sample configuration", location_type="static",
            is_public=False,
            is_internal=True,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II", location_type="static",
            is_public=False,
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

        action1 = DeviceMountAction(
            configuration=configuration1,
            contact=contact,
            device=device1,
            parent_platform=None,
            description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            contact=contact,
            device=device2,
            description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/device-mount-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first configuration
        with self.client:
            url_get_for_configuration1 = (
                base_url + f"/configurations/{configuration1.id}/device-mount-actions"
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
                base_url + f"/configurations/{configuration2.id}/device-mount-actions"
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
                + f"/configurations/{configuration2.id + 9999}/device-mount-actions"
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
            is_internal=True,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II", location_type="static",
            is_public=False,
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

        action1 = DeviceMountAction(
            configuration=configuration1,
            contact=contact,
            device=device1,
            parent_platform=None,
            description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            contact=contact,
            device=device2,
            description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first device
        with self.client:
            url_get_for_device1 = (
                base_url + f"/devices/{device1.id}/device-mount-actions"
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
                base_url + f"/devices/{device2.id}/device-mount-actions"
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
                base_url + f"/devices/{device2.id + 9999}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_device,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_platform(self):
        """Ensure that I can prefilter by a specific (parent) platform."""
        configuration1 = Configuration(
            label="sample configuration", location_type="static",
            is_public=False,
            is_internal=True,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II", location_type="static",
            is_public=False,
            is_internal=True,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(short_name="platform1",
                             is_public=False,
                             is_private=False,
                             is_internal=True,
                             )
        db.session.add(platform1)

        platform2 = Platform(short_name="platform2",
                             is_public=False,
                             is_private=False,
                             is_internal=True,
                             )
        db.session.add(platform2)

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

        action1 = DeviceMountAction(
            configuration=configuration1,
            contact=contact,
            device=device1,
            parent_platform=platform1,
            description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            parent_platform=platform2,
            contact=contact,
            device=device2,
            description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform1.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_platform1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second platform
        with self.client:
            url_get_for_platform2 = (
                base_url + f"/platforms/{platform2.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_platform2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing = (
                base_url + f"/platforms/{platform2.id + 9999}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)
