# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the generic device actions api."""
import json
from datetime import datetime, timezone

from project import base_url, db
from project.api.models import (
    Contact,
    Device,
    GenericDeviceAction,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.models.test_generic_actions_models import (
    generate_device_action_model,
)
from project.tests.permissions import create_a_test_contact, create_a_test_device


def make_generic_device_action_data(object_type, group_ids=None):
    """
    Create the json payload for a generic device action.

    This also creates some associated objects in the database.
    """
    if not group_ids:
        group_ids = []
    device = create_a_test_device(group_ids)
    contact = create_a_test_contact()

    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": fake.paragraph(nb_sentences=3),
                "action_type_name": fake.lexify(
                    text="Random type: ??????????", letters="ABCDE"
                ),
                "action_type_uri": fake.uri(),
                "begin_date": datetime.now().__str__(),
            },
            "relationships": {
                "device": {"data": {"type": "device", "id": device.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
            },
        }
    }
    return data


class TestGenericDeviceActionPermissions(BaseTestCase):
    """Tests for the GenericDeviceAction permissions."""

    url = base_url + "/generic-device-actions"
    object_type = "generic_device_action"

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

    def test_a_public_generic_device_action(self):
        """Ensure a public generic device action will be listed."""
        generic_device_action = generate_device_action_model()
        action = (
            db.session.query(GenericDeviceAction)
            .filter_by(id=generic_device_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_a_internal_generic_device_action(self):
        """Ensure an internal generic device action won't be listed for anonymous."""
        generic_device_action = generate_device_action_model(
            public=False, private=False, internal=True
        )
        action = (
            db.session.query(GenericDeviceAction)
            .filter_by(id=generic_device_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_add_generic_device_action_with_a_permission_group(self):
        """Ensure POST a new generic device action can be added to the database."""
        payload = make_generic_device_action_data(
            self.object_type, group_ids=[str(self.permission_group.id)]
        )
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 201)

    def test_post_for_archived_device(self):
        """Ensure POST a new generic device action cant be added if device is archived."""
        payload = make_generic_device_action_data(
            self.object_type, group_ids=[str(self.permission_group.id)]
        )
        device = db.session.query(Device).order_by("created_at").first()
        device.archived = True
        db.session.add(device)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_post_generic_device_action_data_user_not_in_the_permission_group(self):
        """Post to device,with permission Group different from the user group."""
        payload = make_generic_device_action_data(
            self.object_type, group_ids=[str(self.other_group.id)]
        )
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_action_with_a_permission_group(self):
        """Patch for generic_device_action_data,with permission Group."""
        payload = generate_device_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        self.assertTrue(payload.id is not None)
        generic_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": payload.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{payload.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                url,
                data=json.dumps(generic_device_action_updated),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

    def test_patch_for_archived_device(self):
        """Ensure that we can't patch for archived devices."""
        payload = generate_device_action_model(
            group_ids=[str(self.permission_group.id)],
        )
        device = db.session.query(Device).order_by("created_at").first()
        device.archived = True
        db.session.add(device)
        db.session.commit()

        generic_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": payload.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{payload.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                url,
                data=json.dumps(generic_device_action_updated),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_generic_device_action_data_user_is_not_part_from_permission_group(
        self,
    ):
        """Post to device,with permission Group."""
        generic_device_action = generate_device_action_model(
            group_ids=[str(self.other_group.id)]
        )
        self.assertTrue(generic_device_action.id is not None)
        generic_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": generic_device_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{generic_device_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                url,
                data=json.dumps(generic_device_action_updated),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_generic_device_action_data(self):
        """Delete generic_device_action_data."""
        generic_device_action = generate_device_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        url = f"{self.url}/{generic_device_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_device(self):
        """Ensure we can't delete for archived devices."""
        generic_device_action = generate_device_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        device = db.session.query(Device).order_by("created_at").first()
        device.archived = True
        db.session.add(device)
        db.session.commit()
        url = f"{self.url}/{generic_device_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_generic_device_action_data_as_member(self):
        """Delete generic_device_action_data as member."""
        generic_device_action = generate_device_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        url = f"{self.url}/{generic_device_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

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
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        action = GenericDeviceAction(
            device=device1,
            contact=contact,
            begin_date=datetime(2022, 12, 24, 0, 0, 0, tzinfo=timezone.utc),
            action_type_name="Something",
            action_type_uri="something",
        )
        db.session.add_all([device1, device2, contact, action])
        db.session.commit()

        payload = {
            "data": {
                "type": "generic_device_action",
                "id": action.id,
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
                f"{self.url}/{action.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
