# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test for the api usage for device software update action attachments."""

from project import base_url, db
from project.api.models import (
    Contact,
    Device,
    DeviceAttachment,
    DeviceSoftwareUpdateAction,
)
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.models.test_software_update_actions_attachment_model import (
    add_device_software_update_action_attachment,
)


class TestDeviceSoftwareUpdateActionAttachment(BaseTestCase):
    """Tests for the DeviceSoftwareUpdateActionAttachment endpoints."""

    url = base_url + "/device-software-update-action-attachments"
    object_type = "device_software_update_action_attachment"

    def test_get_device_software_update_action_attachment(self):
        """Ensure the GET /device_software_update_action_attachment route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_software_update_action_attachment_collection(self):
        """Test retrieve a collection of DeviceSoftwareUpdateActionAttachment objects."""
        device_software_update_action_attachment = (
            add_device_software_update_action_attachment()
        )
        device = device_software_update_action_attachment.action.device
        device.is_public = True
        device.is_internal = False
        db.session.add(device)
        db.session.commit()

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"],
            str(device_software_update_action_attachment.id),
        )

    def test_get_device_software_update_action_attachment_collection_internal(self):
        """Ensure we don't give out attachments for internal devices without login."""
        device_software_update_action_attachment = (
            add_device_software_update_action_attachment()
        )
        device = device_software_update_action_attachment.action.device
        self.assertTrue(device.is_internal)

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be empty
        self.assertEqual(response.json["meta"]["count"], 0)

    def test_post_device_software_update_action_attachment(self):
        """Create DeviceSoftwareUpdateActionAttachment."""
        userinfo = generate_userinfo_data()
        device = Device(
            short_name="Device 277",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add(device)
        db.session.commit()
        attachment = DeviceAttachment(
            label=fake.pystr(), url=fake.url(), device_id=device.id
        )
        device_software_update_action = DeviceSoftwareUpdateAction(
            device=device,
            software_type_name=fake.pystr(),
            software_type_uri=fake.uri(),
            update_date=fake.date(),
            version="0.5455",
            repository_url=fake.url(),
            description=fake.paragraph(nb_sentences=3),
            contact=contact,
        )
        db.session.add_all([device, attachment, contact, device_software_update_action])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {
                            "type": "device_software_update_action",
                            "id": device_software_update_action.id,
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

    def test_update_device_software_update_action_attachment(self):
        """Update DeviceSoftwareUpdateActionAttachment."""
        device_software_update_action_attachment = (
            add_device_software_update_action_attachment()
        )
        device = Device(
            short_name="Device new 277",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()
        attachment = DeviceAttachment(
            label=fake.pystr(), url=fake.url(), device_id=device.id
        )
        db.session.add(attachment)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": device_software_update_action_attachment.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {"type": "device_attachment", "id": attachment.id}
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{device_software_update_action_attachment.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_device_software_update_action_attachment(self):
        """Delete DeviceSoftwareUpdateActionAttachment."""
        device_software_update_action_attachment = (
            add_device_software_update_action_attachment()
        )
        _ = super().delete_object(
            url=f"{self.url}/{device_software_update_action_attachment.id}",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
