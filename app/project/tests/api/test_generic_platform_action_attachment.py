from project import base_url
from project.api.models import PlatformAttachment
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_platform_action_attachment_model,
)
from project.tests.models.test_generic_actions_models import generate_platform_action_model


class TestGenericPlatformActionAttachment(BaseTestCase):
    """Tests for the GenericPlatformActionAttachment endpoints."""

    generic_platform_action_attachment_url = (
            base_url + "/generic-platform-action-attachments"
    )
    object_type = "generic_platform_action_attachment"

    def test_get_generic_platform_action_attachment(self):
        """Ensure the GET /generic_platform_action_attachments route reachable."""
        response = self.client.get(self.generic_platform_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_platform_action_attachment_collection(self):
        """Test retrieve a collection of GenericPlatformActionAttachment objects"""
        _ = add_generic_platform_action_attachment_model()
        with self.client:
            response = self.client.get(self.generic_platform_action_attachment_url)
        self.assertEqual(response.status_code, 200)

    def test_post_generic_platform_action_attachment(self):
        """Create GenericPlatformActionAttachment"""
        gpa = generate_platform_action_model()
        a = PlatformAttachment(
            label="test platform attachment",
            url=fake.image_url(),
            platform_id=gpa.platform_id,
        )

        db.session.add(a)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {"data": {"type": "generic_platform_action", "id": gpa.id}},
                    "attachment": {"data": {"type": "platform_attachment", "id": a.id}}, },
            }
        }
        _ = super().add_object(
            url=f"{self.generic_platform_action_attachment_url}?include=action,attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_generic_platform_action_attachment(self):
        """Update GenericPlatformActionAttachment"""
        old = add_generic_platform_action_attachment_model()
        a_new = PlatformAttachment(
            label="new platform attachment",
            url=fake.image_url(),
            platform_id=old.platform_id,
        )

        db.session.add(a_new)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": old.id,
                "attributes": {},
                "relationships": {
                    "attachment": {"data": {"type": "platform_attachment", "id": a_new.id}}, },
            }
        }
        _ = super().update_object(
            url=f"{self.generic_platform_action_attachment_url}/{old.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_generic_platform_action_attachment(self):
        """Delete GenericPlatformActionAttachment """
        dpa_a = add_generic_platform_action_attachment_model()
        _ = super().delete_object(
            url=f"{self.generic_platform_action_attachment_url}/{dpa_a.id}",
        )
