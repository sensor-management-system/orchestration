# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the devices-relationships."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Device
from project.api.models.base_model import db
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token
from project.tests.base import fake
from project.tests.permissions import create_a_test_contact, create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestDeviceRelationshipPermissions(BaseTestCase):
    """Tests for the Device relationship Permissions."""

    def test_fail_adding_relationship_to_device_without_jwt(self):
        """Ensure adding a relationship without a valid token will fail."""
        public_sensor = create_a_test_device(
            public=True,
            private=False,
            internal=False,
        )
        contact = create_a_test_contact()
        db.session.add_all([public_sensor, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/devices/{public_sensor.id}/relationships/contacts"
        with self.client:
            response = self.client.post(
                url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 401)

    def test_success_adding_relationship_to_device_with_no_group(self):
        """Ensure adding a relationship to a no group device will success."""
        public_sensor = create_a_test_device(
            public=True,
            private=False,
            internal=False,
        )
        contact = create_a_test_contact()
        db.session.add_all([public_sensor, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/devices/{public_sensor.id}/relationships/contacts"
        with self.client:
            response = self.client.post(
                url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 200)

    def test_fail_adding_relationship_to_device_with_a_group_other_than_user(self):
        """Ensure adding a relationship will fail if user not involve in parent permission group."""
        public_sensor = create_a_test_device(
            public=True, private=False, internal=False, group_ids=["403"]
        )
        contact = create_a_test_contact()
        db.session.add_all([public_sensor, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/devices/{public_sensor.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_success_adding_relationship_to_device_with_a_group(self):
        """Ensure adding a relationship will success if user in parent permission group."""
        public_sensor = create_a_test_device(
            public=True,
            private=False,
            internal=False,
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups,
        )
        contact = create_a_test_contact()
        db.session.add_all([public_sensor, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/devices/{public_sensor.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_fail_updating_relationship_to_device_with_a_group_other_than_user(self):
        """Ensure updating a relationship will fail if user not involve in parent permission group."""
        public_sensor = create_a_test_device(
            public=True,
            private=False,
            internal=False,
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups,
        )
        contact = create_a_test_contact()
        contact_2 = create_a_test_contact()
        db.session.add_all([public_sensor, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        data_2 = {"data": [{"type": "contact", "id": contact_2.id}]}
        url = base_url + f"/devices/{public_sensor.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response.status_code, 200)

                public_sensor.group_ids = ["403"]
                response_patch = self.client.patch(
                    url,
                    data=json.dumps(data_2),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response_patch.status_code, 403)

    def test_success_updating_relationship_to_device_with_a_group_other_than_user(self):
        """Ensure updating a relationship will fail if user not involve in parent permission group."""
        public_sensor = create_a_test_device(
            public=True,
            private=False,
            internal=False,
            group_ids=IDL_USER_ACCOUNT.membered_permission_groups,
        )
        contact = create_a_test_contact()
        contact_2 = create_a_test_contact()
        db.session.add_all([public_sensor, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        data_2 = {"data": [{"type": "contact", "id": contact_2.id}]}
        url = base_url + f"/devices/{public_sensor.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response.status_code, 200)

                response_patch = self.client.patch(
                    url,
                    data=json.dumps(data_2),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response_patch.status_code, 200)

    def test_fail_delete_a_relationship_to_device_with_a_group_other_than_user(self):
        """Ensure Deletion fails if user not in parent permission group."""
        contact = create_a_test_contact()
        public_sensor = Device(
            short_name="test",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
            group_ids=["403"],
            contacts=[contact],
        )

        db.session.add_all([public_sensor, contact])
        db.session.commit()
        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/devices/{public_sensor.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)
