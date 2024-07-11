# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the api usage for generic device action attachments."""
from project import base_url
from project.api.models import DeviceAttachment
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_device_action_model,
)
from project.tests.models.test_generic_actions_models import (
    generate_device_action_model,
)


class TestGenericDeviceActionAttachment(BaseTestCase):
    """Tests for the GenericDeviceActionAttachment endpoints."""

    url = base_url + "/generic-device-action-attachments"
    object_type = "generic_device_action_attachment"

    def test_get_generic_device_action_attachment(self):
        """Ensure the GET /generic_device_action_attachments route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_device_action_attachment_collection(self):
        """Test retrieve a collection of GenericDeviceActionAttachment objects."""
        generic_device_action = add_generic_device_action_model()
        self.assertTrue(generic_device_action.device.is_public)
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"],
            str(generic_device_action.generic_device_action_attachments[0].id),
        )

    def test_get_generic_device_action_attachment_collection_internal(self):
        """Ensure we don't expose details if the device is internal without user login."""
        generic_device_action = add_generic_device_action_model()
        device = generic_device_action.device
        device.is_internal = True
        device.is_public = False
        db.session.add(device)
        db.session.commit()

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["meta"]["count"], 0)

    def test_post_generic_device_action_attachment(self):
        """Create GenericDeviceActionAttachment."""
        device_action = generate_device_action_model()
        attachment = DeviceAttachment(
            label="test device attachment",
            url=fake.image_url(),
            device_id=device_action.device_id,
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
                            "type": "generic_device_action",
                            "id": device_action.id,
                        }
                    },
                    "attachment": {
                        "data": {"type": "device_attachment", "id": attachment.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=action,attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_generic_device_action_attachment(self):
        """Update GenericDeviceActionAttachment."""
        generic_device_action = add_generic_device_action_model()
        attachment_new = DeviceAttachment(
            label="new device attachment",
            url=fake.image_url(),
            device_id=generic_device_action.device_id,
        )
        db.session.add(attachment_new)
        db.session.commit()
        generic_device_action_attachment = (
            generic_device_action.generic_device_action_attachments[0]
        )
        data = {
            "data": {
                "type": self.object_type,
                "id": generic_device_action_attachment.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {"type": "device_attachment", "id": attachment_new.id}
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{generic_device_action_attachment.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_generic_device_action_attachment(self):
        """Delete GenericDeviceActionAttachment."""
        generic_device_action = add_generic_device_action_model()
        generic_device_action_attachment = (
            generic_device_action.generic_device_action_attachments[0]
        )
        _ = super().delete_object(
            url=f"{self.url}/{generic_device_action_attachment.id}",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
