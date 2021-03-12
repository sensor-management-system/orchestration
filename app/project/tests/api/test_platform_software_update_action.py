from project import base_url, db
from project.api.models import Contact, Platform
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_software_update_actions_model import (
    add_platform_software_update_action_model,
)


class TestPlatformSoftwareUpdateAction(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateAction endpoints."""

    url = base_url + "/platform-software-update-actions"
    object_type = "platform_software_update_action"

    def test_get_platform_software_update_action(self):
        """Ensure the GET /platform_software_update_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_software_update_action_collection(self):
        """Test retrieve a collection of PlatformSoftwareUpdateAction objects"""
        _ = add_platform_software_update_action_model()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_platform_software_update_action(self):
        """Create PlatformSoftwareUpdateAction"""
        platform = Platform(short_name="Platform 111")
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        db.session.add_all([platform, contact])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test platform_software_update_action",
                    "version": f"v_{fake.pyint()}",
                    "software_type_name": fake.pystr(),
                    "software_type_uri": fake.uri(),
                    "repository_url": fake.url(),
                    "update_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": platform.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=platform,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_platform_software_update_action(self):
        """Update PlatformSoftwareUpdateAction"""
        platform_software_update_action = add_platform_software_update_action_model()
        platform_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{platform_software_update_action.id}",
            data_object=platform_software_update_action_updated,
            object_type=self.object_type,
        )

    def test_delete_platform_software_update_action(self):
        """Delete PlatformSoftwareUpdateAction """
        platform_software_update_action = add_platform_software_update_action_model()
        _ = super().delete_object(
            url=f"{self.url}/{platform_software_update_action.id}",
        )
