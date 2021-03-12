import json

from project import base_url
from project.api.models import Contact, Platform
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
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
        """Test retrieve a collection of PlatformUnmountAction objects"""
        unmount_platform_action = add_unmount_platform_action()
        response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            unmount_platform_action.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            data["data"][0]["attributes"]["end_date"],
        )

    def test_post_platform_unmount_action(self):
        """Create PlatformUnmountAction"""
        platform = Platform(
            short_name="Test platform",
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
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
        """Update PlatformUnmountAction"""
        unmount_platform_action = add_unmount_platform_action()
        unmount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": unmount_platform_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{unmount_platform_action.id}",
            data_object=unmount_platform_action_updated,
            object_type=self.object_type,
        )

    def test_delete_platform_unmount_action(self):
        """Delete PlatformUnmountAction """
        unmount_platform_action = add_unmount_platform_action()
        _ = super().delete_object(
            url=f"{self.url}/{unmount_platform_action.id}",
        )
