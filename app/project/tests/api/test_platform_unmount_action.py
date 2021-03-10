import json

from project import base_url
from project.api.models import (
    Contact,
    Platform,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.models.test_unmount_actions_model import add_unmount_platform_action

from project.tests.base import generate_token_data, fake
from project.tests.models.test_configurations_model import generate_configuration_model


class TestPlatformUnmountAction(BaseTestCase):
    """Tests for the PlatformUnmountAction endpoints."""

    platform_unmount_action_url = base_url + "/platform-unmount-actions"
    object_type = "platform_unmount_action"

    def test_get_platform_unmount_action(self):
        """Ensure the GET /platform_unmount_actions route reachable."""
        response = self.client.get(self.platform_unmount_action_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_unmount_action_collection(self):
        """Test retrieve a collection of PlatformUnmountAction objects"""
        uda = add_unmount_platform_action()
        response = self.client.get(self.platform_unmount_action_url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(uda.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                         data["data"][0]["attributes"]["end_date"])

    def test_post_platform_unmount_action(self):
        """Create PlatformUnmountAction"""
        p = Platform(
            short_name="Test platform",
        )
        p_p = Platform(
            short_name="parent platform",
        )
        jwt1 = generate_token_data()
        c1 = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        config = generate_configuration_model()
        db.session.add_all([p, p_p, c1, config])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "test unmount platform action",
                    "end_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": p.id}},
                    "contact": {"data": {"type": "contact", "id": c1.id}},
                    "configuration": {"data": {"type": "configuration", "id": config.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.platform_unmount_action_url}?include=platform,contact,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_platform_unmount_action(self):
        """Update PlatformUnmountAction"""
        upa = add_unmount_platform_action()
        c_updated = {
            "data": {
                "type": self.object_type,
                "id": upa.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.platform_unmount_action_url}/{upa.id}",
            data_object=c_updated,
            object_type=self.object_type,
        )

    def test_delete_platform_unmount_action(self):
        """Delete PlatformUnmountAction """
        upa = add_unmount_platform_action()
        _ = super().delete_object(
            url=f"{self.platform_unmount_action_url}/{upa.id}",
        )
