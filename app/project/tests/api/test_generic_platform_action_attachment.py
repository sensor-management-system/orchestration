from project import base_url
from project.api.models import PlatformAttachment
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_platform_action_attachment_model,
)
from project.tests.models.test_generic_actions_models import (
    generate_platform_action_model,
)


class TestGenericPlatformActionAttachment(BaseTestCase):
    """Tests for the GenericPlatformActionAttachment endpoints."""

    url = base_url + "/generic-platform-action-attachments"
    object_type = "generic_platform_action_attachment"

    def test_get_generic_platform_action_attachment(self):
        """Ensure the GET /generic_platform_action_attachments route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_platform_action_attachment_collection(self):
        """Test retrieve a collection of GenericPlatformActionAttachment objects"""
        _ = add_generic_platform_action_attachment_model()
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_generic_platform_action_attachment(self):
        """Create GenericPlatformActionAttachment"""
        platform_action = generate_platform_action_model()
        attachment = PlatformAttachment(
            label="test platform attachment",
            url=fake.image_url(),
            platform_id=platform_action.platform_id,
        )

        db.session.add(attachment)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {
                            "type": "generic_platform_action",
                            "id": platform_action.id,
                        }
                    },
                    "attachment": {
                        "data": {"type": "platform_attachment", "id": attachment.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=action,attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_generic_platform_action_attachment(self):
        """Update GenericPlatformActionAttachment"""
        generic_platform_action_attachment = (
            add_generic_platform_action_attachment_model()
        )
        generic_platform_action_attachment_changed = PlatformAttachment(
            label="new platform attachment",
            url=fake.image_url(),
            platform_id=generic_platform_action_attachment.platform_id,
        )

        db.session.add(generic_platform_action_attachment_changed)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": generic_platform_action_attachment.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {
                            "type": "platform_attachment",
                            "id": generic_platform_action_attachment_changed.id,
                        }
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{generic_platform_action_attachment.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_generic_platform_action_attachment(self):
        """Delete GenericPlatformActionAttachment """
        generic_platform_action_attachment = (
            add_generic_platform_action_attachment_model()
        )
        url = f"{self.url}/{generic_platform_action_attachment.id}"
        _ = super().delete_object(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
