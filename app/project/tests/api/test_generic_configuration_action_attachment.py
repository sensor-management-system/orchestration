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

    generic_configuration_action_attachment_url = (
        base_url + "/generic-configuration-action-attachments"
    )
    object_type = "generic_configuration_action_attachment"

    def test_get_generic_configuration_action_attachment(self):
        """Ensure the GET /generic_configuration_action_attachments route reachable."""
        response = self.client.get(self.generic_configuration_action_attachment_url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_configuration_action_attachment_collection(self):
        """Test retrieve a collection of GenericConfigurationActionAttachment objects"""
        _ = add_generic_configuration_action_attachment_model()
        with self.client:
            response = self.client.get(self.generic_configuration_action_attachment_url)
        _ = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_post_generic_configuration_action_attachment(self):
        """Create GenericConfigurationActionAttachment"""
        gca = generate_configuration_action_model()
        a1 = ConfigurationAttachment(
            label="configuration attachment1",
            url=fake.image_url(),
            configuration_id=gca.configuration_id,
        )
        db.session.add(a1)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {"type": "generic_configuration_action", "id": gca.id}
                    },
                    "attachment": {
                        "data": {"type": "configuration_attachment", "id": a1.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.generic_configuration_action_attachment_url}?include=action,attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_generic_configuration_action_attachment(self):
        """Update GenericConfigurationActionAttachment"""
        old = add_generic_configuration_action_attachment_model()
        a = ConfigurationAttachment(
            label="configuration attachment1",
            url=fake.image_url(),
            configuration_id=old.configuration_id,
        )
        db.session.add(a)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": old.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {"type": "configuration_attachment", "id": a.id}
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.generic_configuration_action_attachment_url}/{old.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_generic_configuration_action_attachment(self):
        """Delete GenericConfigurationActionAttachment """
        gca_a = add_generic_configuration_action_attachment_model()
        _ = super().delete_object(
            url=f"{self.generic_configuration_action_attachment_url}/{gca_a.id}",
        )

    def test_post_generic_configuration_action_attachment_false_type(self):
        """Check errors.
        This should give a Validation error with code 422.
        """
        gca = generate_configuration_action_model()
        a1 = ConfigurationAttachment(
            label="configuration attachment1",
            url=fake.image_url(),
            configuration_id=gca.configuration_id,
        )
        db.session.add(a1)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {"type": "generic_configuration_action", "id": gca.id}
                    },
                    "attachment": {"data": {"type": "device_attachment", "id": a1.id}},
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.generic_configuration_action_attachment_url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        self.assertEqual(response.status_code, 422)
