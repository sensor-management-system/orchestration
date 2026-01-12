# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the permission handling for device properties."""

import json

from project import base_url
from project.api.models import (
    Contact,
    Device,
    DeviceAttachment,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_device


def prepare_device_attachment_payload(device):
    """Create some payload to send on the backend."""
    payload = {
        "data": {
            "type": "device_attachment",
            "attributes": {"label": fake.pystr(), "url": fake.url()},
            "relationships": {
                "device": {"data": {"type": "device", "id": str(device.id)}}
            },
        }
    }
    return payload


class TesDeviceAttachment(BaseTestCase):
    """Test DeviceAttachment."""

    url = base_url + "/device-attachments"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)
        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                normal_contact,
                self.normal_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_get_public_device_attachments(self):
        """Ensure that we can get a list of public device_attachments."""
        device1 = create_a_test_device(
            public=True,
            private=False,
            internal=False,
        )
        device2 = create_a_test_device(
            public=True,
            private=False,
            internal=False,
        )

        attachment1 = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device1,
        )
        attachment2 = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device1,
        )
        attachment3 = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device2,
        )

        db.session.add_all([attachment1, attachment2, attachment3])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_device_attachments(self):
        """Ensure that we can get a list of internal device_attachments only with a valid jwt."""
        device1 = create_a_test_device(
            public=False,
            private=False,
            internal=True,
        )
        device2 = create_a_test_device(
            public=False,
            private=False,
            internal=True,
        )

        attachment1 = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device1,
        )
        attachment2 = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device2,
        )

        db.session.add_all([attachment1, attachment2])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

    def test_post_to_a_device_with_a_permission_group(self):
        """Post to device,with permission Group."""
        device = create_a_test_device([str(self.permission_group.id)])
        self.assertTrue(device.id is not None)
        count_device_attachments = (
            db.session.query(DeviceAttachment)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_device_attachments, 0)
        payload = prepare_device_attachment_payload(device)
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 201)
        device_attachments = query_result_to_list(
            db.session.query(DeviceAttachment).filter_by(
                device_id=device.id,
            )
        )
        self.assertEqual(len(device_attachments), 1)

        attachment = device_attachments[0]
        self.assertEqual(attachment.label, payload["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, payload["data"]["attributes"]["url"])
        self.assertEqual(attachment.device_id, device.id)
        self.assertEqual(str(attachment.device_id), response.get_json()["data"]["id"])

    def test_post_to_archived_device(self):
        """Ensure that we can't post for an archived device."""
        device = create_a_test_device([str(self.permission_group.id)])
        device.archived = True
        db.session.add(device)
        db.session.commit()
        payload = prepare_device_attachment_payload(device)
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_post_to_a_device_with_an_other_permission_group(self):
        """Post to a device with a different permission Group from the user."""
        device = create_a_test_device([str(self.other_group.id)])
        self.assertTrue(device.id is not None)
        count_device_attachments = (
            db.session.query(DeviceAttachment)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_device_attachments, 0)
        payload = prepare_device_attachment_payload(device)
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_device_with_a_permission_group(self):
        """Patch attachment of device with same group as user."""
        device = create_a_test_device([str(self.permission_group.id)])
        self.assertTrue(device.id is not None)
        count_device_attachments = (
            db.session.query(DeviceAttachment)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_device_attachments, 0)
        attachment = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device,
        )
        db.session.add(attachment)
        db.session.commit()
        payload = {
            "data": {
                "id": attachment.id,
                "type": "device_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(attachment.label, data["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])
        self.assertEqual(attachment.device_id, device.id)

    def test_patch_for_archived_device(self):
        """Ensure we can't patch for an archived device."""
        device = create_a_test_device([str(self.permission_group.id)])
        attachment = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device,
        )
        device.archived = True
        db.session.add_all([attachment, device])
        db.session.commit()
        payload = {
            "data": {
                "id": attachment.id,
                "type": "device_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_device_with_a_permission_group(self):
        """Delete attachment of device with same group as user (user is member)."""
        device = create_a_test_device([str(self.permission_group.id)])
        self.assertTrue(device.id is not None)
        count_device_attachments = (
            db.session.query(DeviceAttachment)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_device_attachments, 0)
        attachment = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device,
        )
        db.session.add(attachment)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_device(self):
        """Ensure we can't delete for an archived device."""
        device = create_a_test_device([str(self.permission_group.id)])
        attachment = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device,
        )
        device.archived = True
        db.session.add_all([attachment, device])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = self.url + "/" + str(attachment.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_non_editable_device(self):
        """Ensure we can't update to a device we can't edit."""
        device1 = Device(
            short_name="device1",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=[str(self.permission_group.id)],
        )
        device2 = Device(
            short_name="device2",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=[str(self.other_group.id)],
        )
        attachment = DeviceAttachment(
            label="k",
            url="v",
            device=device1,
        )
        db.session.add_all([device1, device2, attachment])
        db.session.commit()

        payload = {
            "data": {
                "type": "device_attachment",
                "id": attachment.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another device for
                    # which we have no edit permissions.
                    "device": {
                        "data": {
                            "type": "device",
                            "id": device2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{attachment.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
