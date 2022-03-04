"""Test for the platform unmount actions api."""

import json

from project import base_url
from project.api.models import Configuration, Contact, Platform, PlatformUnmountAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.base import create_token
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_unmount_actions_model import add_unmount_platform_action


class TestPlatformUnmountAction(BaseTestCase):
    """Tests for the PlatformUnmountAction endpoints."""

    url = base_url + "/platform-unmount-actions"
    object_type = "platform_unmount_action"

    def test_get_platform_unmount_action(self):
        """Ensure the GET /platform_unmount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_unmount_action_collection(self):
        """Test retrieve a collection of PlatformUnmountAction objects."""
        unmount_platform_action = add_unmount_platform_action()
        response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            unmount_platform_action.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            data["data"][0]["attributes"]["end_date"],
        )

    def test_post_platform_unmount_action(self):
        """Create PlatformUnmountAction."""
        platform = Platform(
            short_name="Test platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        config = generate_configuration_model()
        db.session.add_all([platform, contact, config])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "test unmount platform action",
                    "end_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": platform.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=platform,contact,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_platform_unmount_action(self):
        """Update PlatformUnmountAction."""
        unmount_platform_action = add_unmount_platform_action()
        unmount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": unmount_platform_action.id,
                "attributes": {"description": "updated", },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{unmount_platform_action.id}",
            data_object=unmount_platform_action_updated,
            object_type=self.object_type,
        )

    def test_delete_platform_unmount_action(self):
        """Delete PlatformUnmountAction."""
        unmount_platform_action = add_unmount_platform_action()

        access_headers = create_token()
        with self.client:
            response = self.client.delete(
                f"{self.url}/{unmount_platform_action.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertNotEqual(response.status_code, 200)

    def test_filtered_by_configuration(self):
        """Ensure that I can prefilter by a specific configuration."""
        configuration1 = Configuration(
            label="sample configuration",
            location_type="static",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            location_type="static",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(
            short_name="platform1", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform1)

        platform2 = Platform(
            short_name="platform2", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform2)

        action1 = PlatformUnmountAction(
            configuration=configuration1,
            contact=contact,
            platform=platform1,
            description="Some first action",
            end_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformUnmountAction(
            configuration=configuration2,
            contact=contact,
            platform=platform2,
            description="Some other action",
            end_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/platform-unmount-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first configuration
        with self.client:
            url_get_for_configuration1 = (
                    base_url
                    + f"/configurations/{configuration1.id}/platform-unmount-actions"
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
                    base_url
                    + f"/configurations/{configuration2.id}/platform-unmount-actions"
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
                    + f"/configurations/{configuration2.id + 9999}/platform-unmount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_configuration,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_platform(self):
        """Ensure that I can prefilter by a specific platforms."""
        configuration1 = Configuration(
            label="sample configuration",
            location_type="static",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            location_type="static",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(
            short_name="platform1", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform1)

        platform2 = Platform(
            short_name="platform2", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform2)

        action1 = PlatformUnmountAction(
            configuration=configuration1,
            contact=contact,
            platform=platform1,
            description="Some first action",
            end_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformUnmountAction(
            configuration=configuration2,
            contact=contact,
            platform=platform2,
            description="Some other action",
            end_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                    base_url + f"/platforms/{platform1.id}/platform-unmount-actions"
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
                    base_url + f"/platforms/{platform2.id}/platform-unmount-actions"
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
            url_get_for_non_existing_platform = (
                    base_url + f"/platforms/{platform2.id + 9999}/platform-unmount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_platform,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
