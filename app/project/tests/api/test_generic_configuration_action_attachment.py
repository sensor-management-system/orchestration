import json

from project import base_url, db
from project.api.models import ConfigurationAttachment
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_configuration_action_attachment_model,
)
from project.tests.models.test_generic_actions_models import (
    generate_configuration_action_model,
)


class TestGenericConfigurationActionAttachment(BaseTestCase):
    """Tests for the GenericConfigurationActionAttachment endpoints."""

    url = base_url + "/generic-configuration-action-attachments"
    object_type = "generic_configuration_action_attachment"

    def test_get_generic_configuration_action_attachment(self):
        """Ensure the GET /generic_configuration_action_attachments route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_configuration_action_attachment_collection(self):
        """Test retrieve a collection of GenericConfigurationActionAttachment objects"""
        generic_configuration_action_attachment = (
            add_generic_configuration_action_attachment_model()
        )
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"],
            str(generic_configuration_action_attachment.id),
        )

    def test_post_generic_configuration_action_attachment(self):
        """Create GenericConfigurationActionAttachment"""
        generic_configuration_action = generate_configuration_action_model()
        a1 = ConfigurationAttachment(
            label="configuration attachment1",
            url=fake.image_url(),
            configuration_id=generic_configuration_action.configuration_id,
        )
        db.session.add(a1)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {
                            "type": "generic_configuration_action",
                            "id": generic_configuration_action.id,
                        }
                    },
                    "attachment": {
                        "data": {"type": "configuration_attachment", "id": a1.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=action,attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_generic_configuration_action_attachment(self):
        """Update GenericConfigurationActionAttachment"""
        generic_configuration_action_attachment = (
            add_generic_configuration_action_attachment_model()
        )
        attachment = ConfigurationAttachment(
            label="configuration attachment1",
            url=fake.image_url(),
            configuration_id=generic_configuration_action_attachment.configuration_id,
        )
        db.session.add(attachment)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": generic_configuration_action_attachment.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {
                            "type": "configuration_attachment",
                            "id": attachment.id,
                        }
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{generic_configuration_action_attachment.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_generic_configuration_action_attachment(self):
        """Delete GenericConfigurationActionAttachment """
        generic_configuration_action_attachment = (
            add_generic_configuration_action_attachment_model()
        )
        _ = super().delete_object(
            url=f"{self.url}/{generic_configuration_action_attachment.id}",
        )

    def test_post_generic_configuration_action_attachment_false_type(self):
        """Check errors.
        This should give a Validation error with code 422.
        """
        configuration_action = generate_configuration_action_model()
        a1 = ConfigurationAttachment(
            label="configuration attachment1",
            url=fake.image_url(),
            configuration_id=configuration_action.configuration_id,
        )
        db.session.add(a1)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {
                            "type": "generic_configuration_action",
                            "id": configuration_action.id,
                        }
                    },
                    "attachment": {"data": {"type": "device_attachment", "id": a1.id}},
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        self.assertEqual(response.status_code, 422)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
