# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test cases for the api usage for generic platform action attachments."""

import json

from project import base_url
from project.api.models import PlatformAttachment
from project.api.models.base_model import db
from project.extensions.instances import mqtt
from project.tests.base import BaseTestCase, fake
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_platform_action_model,
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
        """Test retrieve a collection of GenericPlatformActionAttachment objects."""
        generic_platform_action = add_generic_platform_action_model()
        self.assertTrue(generic_platform_action.platform.is_public)
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"],
            str(generic_platform_action.generic_platform_action_attachments[0].id),
        )

    def test_get_generic_platform_action_attachment_collection_internal(self):
        """Ensure we don't expose details if the platform is internal without user login."""
        generic_platform_action = add_generic_platform_action_model()
        platform = generic_platform_action.platform
        platform.is_internal = True
        platform.is_public = False
        db.session.add(platform)
        db.session.commit()

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["meta"]["count"], 0)

    def test_post_generic_platform_action_attachment(self):
        """Create GenericPlatformActionAttachment."""
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
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal(
            "sms/post-generic-platform-action-attachment"
        )
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal(
            "generic_platform_action_attachment"
        )
        self.expect(
            notification_data["relationships"]["action"]["data"]["id"]
        ).to_equal(str(platform_action.id))
        self.expect(str).of(notification_data["id"]).to_match(r"\d+")

    def test_update_generic_platform_action_attachment(self):
        """Update GenericPlatformActionAttachment."""
        generic_platform_action = add_generic_platform_action_model()
        attachment_new = PlatformAttachment(
            label="new platform attachment",
            url=fake.image_url(),
            platform_id=generic_platform_action.platform_id,
        )
        db.session.add(attachment_new)
        db.session.commit()
        generic_platform_action_attachment = (
            generic_platform_action.generic_platform_action_attachments[0]
        )
        data = {
            "data": {
                "type": self.object_type,
                "id": generic_platform_action_attachment.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {"type": "platform_attachment", "id": attachment_new.id}
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{generic_platform_action_attachment.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal(
            "sms/patch-generic-platform-action-attachment"
        )
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal(
            "generic_platform_action_attachment"
        )
        self.expect(
            notification_data["relationships"]["attachment"]["data"]["id"]
        ).to_equal(str(attachment_new.id))
        self.expect(
            notification_data["relationships"]["action"]["data"]["id"]
        ).to_equal(str(generic_platform_action_attachment.action_id))

    def test_delete_generic_platform_action_attachment(self):
        """Delete GenericPlatformActionAttachment."""
        generic_platform_action = add_generic_platform_action_model()
        generic_platform_action_attachment = (
            generic_platform_action.generic_platform_action_attachments[0]
        )
        _ = super().delete_object(
            url=f"{self.url}/{generic_platform_action_attachment.id}",
        )
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal(
            "sms/delete-generic-platform-action-attachment"
        )
        self.expect(json.loads).of(call_args[1]).to_equal(
            {
                "data": {
                    "type": "generic_platform_action_attachment",
                    "id": str(generic_platform_action_attachment.id),
                }
            }
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
