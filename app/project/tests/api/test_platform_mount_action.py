"""Tests for the platform mount action api."""
import json

from project import base_url
from project.api.models import Configuration, Contact, Platform, PlatformMountAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_mount_actions_model import (
    add_mount_platform_action_model,
)


class TestPlatformMountAction(BaseTestCase):
    """Tests for the PlatformMountAction endpoints."""

    url = base_url + "/platform-mount-actions"
    object_type = "platform_mount_action"

    def test_filtered_by_configuration(self):
        """Ensure that I can prefilter by a specific configuration."""
        configuration1 = Configuration(
            label="sample configuration", location_type="static"
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II", location_type="static"
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(short_name="platform1")
        db.session.add(platform1)

        platform2 = Platform(short_name="Platform2")
        db.session.add(platform2)

        action1 = PlatformMountAction(
            configuration=configuration1,
            contact=contact,
            parent_platform=None,
            platform=platform1,
            description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformMountAction(
            configuration=configuration2,
            contact=contact,
            platform=platform2,
            parent_platform=None,
            description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/platform-mount-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first configuration
        with self.client:
            url_get_for_configuration1 = (
                base_url + f"/configurations/{configuration1.id}/platform-mount-actions"
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
                base_url + f"/configurations/{configuration2.id}/platform-mount-actions"
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
                + f"/configurations/{configuration2.id + 9999}/platform-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_configuration,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_platform(self):
        """Ensure that I can prefilter by a specific platform."""
        configuration1 = Configuration(
            label="sample configuration", location_type="static"
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II", location_type="static"
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(short_name="platform1")
        db.session.add(platform1)

        platform2 = Platform(short_name="Platform2")
        db.session.add(platform2)

        action1 = PlatformMountAction(
            configuration=configuration1,
            contact=contact,
            parent_platform=None,
            platform=platform1,
            description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformMountAction(
            configuration=configuration2,
            contact=contact,
            platform=platform2,
            parent_platform=None,
            description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform1.id}/platform-mount-actions"
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
                base_url + f"/platforms/{platform2.id}/platform-mount-actions"
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
                base_url + f"/platforms/{platform2.id + 9999}/platform-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_parent_platform(self):
        """Ensure filter by a specific parent platform works well."""
        configuration1 = Configuration(
            label="sample configuration", location_type="static"
        )

        configuration2 = Configuration(
            label="sample configuration II", location_type="static"
        )

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )

        platform1 = Platform(short_name="platform1")

        platform2 = Platform(short_name="Platform2")

        platform3 = Platform(short_name="platform3")

        platform4 = Platform(short_name="Platform4")

        action1 = PlatformMountAction(
            configuration=configuration1,
            contact=contact,
            parent_platform=platform3,
            platform=platform1,
            description="Some first action",
            begin_date=fake.date_time(),
        )

        action2 = PlatformMountAction(
            configuration=configuration2,
            contact=contact,
            platform=platform2,
            parent_platform=platform4,
            description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add_all(
            [
                configuration1,
                configuration2,
                contact,
                platform1,
                platform2,
                platform3,
                platform4,
                action1,
                action2,
            ]
        )
        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform3.id}/parent-platform-mount-actions"
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
                base_url + f"/platforms/{platform4.id}/parent-platform-mount-actions"
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
                base_url
                + f"/platforms/{platform2.id + 9999}/parent-platform-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_get_platform_mount_action(self):
        """Ensure the GET /platform_mount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platfrom_mount_action_collection(self):
        """Test retrieve a collection of PlatformMountAction objects."""
        mount_platform_action = add_mount_platform_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mount_platform_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_platfrom_mount_action(self):
        """Create PlatformMountAction."""
        platform = Platform(
            short_name=fake.linux_processor(),
        )
        parent_platform = Platform(
            short_name="platform parent-platform",
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = generate_configuration_model()
        db.session.add_all([platform, parent_platform, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test PlatformMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": platform.id}},
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
            url=f"{self.url}?include=platform,contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_mount_action(self):
        """Update PlatformMountAction."""
        mount_platform_action = add_mount_platform_action_model()
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_platform_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{mount_platform_action.id}",
            data_object=mount_platform_action_updated,
            object_type=self.object_type,
        )

    def test_delete_device_mount_action(self):
        """Delete PlatformMountAction."""
        mount_platform_action = add_mount_platform_action_model()
        _ = super().delete_object(
            url=f"{self.url}/{mount_platform_action.id}",
        )
