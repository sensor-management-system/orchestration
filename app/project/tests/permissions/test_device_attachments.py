# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the permission handling for device properties."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Device, DeviceAttachment, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


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
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
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
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        device.archived = True
        db.session.add(device)
        db.session.commit()
        payload = prepare_device_attachment_payload(device)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_post_to_a_device_with_an_other_permission_group(self):
        """Post to a device with a different permission Group from the user."""
        device = create_a_test_device([403])
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_device_with_a_permission_group(self):
        """Patch attachment of device with same group as user."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(attachment.label, data["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])
        self.assertEqual(attachment.device_id, device.id)

    def test_patch_for_archived_device(self):
        """Ensure we can't patch for an archived device."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_device_with_a_permission_group(self):
        """Delete attachment of device with same group as user (user is admin)."""
        device = create_a_test_device(IDL_USER_ACCOUNT.administrated_permission_groups)
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_device(self):
        """Ensure we can't delete for an archived device."""
        device = create_a_test_device(IDL_USER_ACCOUNT.administrated_permission_groups)
        attachment = DeviceAttachment(
            label=fake.pystr(),
            url=fake.url(),
            device=device,
        )
        device.archived = True
        db.session.add_all([attachment, device])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_device_with_a_permission_group_as_a_member(self):
        """Delete attachment of device with same group as user (user is member)."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
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
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)
        device_reloaded = (
            db.session.query(Device)
            .filter_by(
                id=device.id,
            )
            .first()
        )
        self.assertEqual(device_reloaded.update_description, "delete;attachment")

    def test_patch_to_non_editable_device(self):
        """Ensure we can't update to a device we can't edit."""
        device1 = Device(
            short_name="device1",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=["1"],
        )
        device2 = Device(
            short_name="device2",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=["2"],
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        attachment = DeviceAttachment(
            label="k",
            url="v",
            device=device1,
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([device1, device2, contact, user, attachment])
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

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*device1.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{attachment.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
