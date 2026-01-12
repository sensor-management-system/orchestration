# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the custom field endpoints."""

import json

from project import base_url
from project.api.models import (
    Contact,
    CustomField,
    Device,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_device


def prepare_custom_field_payload(device):
    """Create some payload to send to the backend."""
    payload = {
        "data": {
            "type": "customfield",
            "attributes": {
                "value": fake.pystr(),
                "key": fake.pystr(),
            },
            "relationships": {
                "device": {"data": {"type": "device", "id": str(device.id)}}
            },
        }
    }
    return payload


class TestCustomFieldServices(BaseTestCase):
    """Test customfields."""

    url = base_url + "/customfields"

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

    def test_get_public_customfields(self):
        """Ensure that we can get a list of public customfields."""
        device1 = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device1,
        )
        customfield2 = CustomField(
            key="UFZ",
            value="https://www.ufz.de",
            device=device1,
        )
        customfield3 = CustomField(
            key="PIK",
            value="https://www.pik-potsdam.de",
            device=device2,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.add(customfield3)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_customfields(self):
        """Ensure that we can get a list of internal customfields only with a valid jwt."""
        device1 = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        device2 = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device1,
        )
        customfield2 = CustomField(
            key="UFZ",
            value="https://www.ufz.de",
            device=device1,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
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
        count_customfields = (
            db.session.query(CustomField)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        payload = prepare_custom_field_payload(device)
        with self.run_requests_as(self.normal_user):
            url_post = base_url + "/customfields"

            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 201)
        customfields = query_result_to_list(
            db.session.query(CustomField).filter_by(
                device_id=device.id,
            )
        )
        self.assertEqual(len(customfields), 1)

        customfield = customfields[0]
        self.assertEqual(customfield.value, payload["data"]["attributes"]["value"])
        self.assertEqual(customfield.key, payload["data"]["attributes"]["key"])
        self.assertEqual(customfield.device_id, device.id)
        self.assertEqual(
            str(customfield.device_id),
            response.get_json()["data"]["relationships"]["device"]["data"]["id"],
        )

    def test_post_for_archived_device(self):
        """Ensure we can't post for an archived device."""
        device = create_a_test_device([str(self.permission_group.id)])
        device.archived = True
        db.session.add(device)
        db.session.commit()
        payload = prepare_custom_field_payload(device)
        with self.run_requests_as(self.normal_user):
            url_post = base_url + "/customfields"

            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 403)

    def test_post_to_a_device_with_an_other_permission_group(self):
        """Post to a device with a different permission Group from the user."""
        device = create_a_test_device([str(self.other_group.id)])
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        payload = prepare_custom_field_payload(device)
        with self.run_requests_as(self.normal_user):
            url_post = base_url + "/customfields"

            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_device_with_a_permission_group(self):
        """Patch Custom field attached to device with same group as user."""
        device = create_a_test_device([str(self.permission_group.id)])
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        customfield = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device,
        )
        db.session.add(customfield)
        db.session.commit()
        payload = {
            "data": {
                "id": customfield.id,
                "type": "customfield",
                "attributes": {"value": "changed", "key": customfield.key},
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = base_url + "/customfields/" + str(customfield.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(customfield.value, data["data"]["attributes"]["value"])
        self.assertEqual(customfield.key, data["data"]["attributes"]["key"])
        self.assertEqual(customfield.device_id, device.id)

    def test_patch_for_archived_device(self):
        """Ensure we can't patch for an archived device."""
        device = create_a_test_device([str(self.permission_group.id)])
        customfield = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device,
        )
        device.archived = True
        db.session.add_all([customfield, device])
        db.session.commit()
        payload = {
            "data": {
                "id": customfield.id,
                "type": "customfield",
                "attributes": {"value": "changed", "key": customfield.key},
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            url = base_url + "/customfields/" + str(customfield.id)

            response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_device_with_a_permission_group(self):
        """Delete customfield for device as group member."""
        device = create_a_test_device([str(self.permission_group.id)])
        self.assertTrue(device.id is not None)
        count_customfields = (
            db.session.query(CustomField)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )

        self.assertEqual(count_customfields, 0)
        customfield = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device,
        )
        db.session.add(customfield)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = base_url + "/customfields/" + str(customfield.id)

            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        reloaded_device = db.session.query(Device).filter_by(id=device.id).first()
        self.assertEqual(reloaded_device.update_description, "delete;custom field")

    def test_delete_for_archived_device(self):
        """Ensure we can't delete for an archived device."""
        device = create_a_test_device([str(self.permission_group.id)])
        customfield = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device,
        )
        device.archived = True
        db.session.add_all([customfield, device])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            url = base_url + "/customfields/" + str(customfield.id)

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
        custom_field = CustomField(
            key="k",
            value="v",
            device=device1,
        )
        db.session.add_all([device1, device2, custom_field])
        db.session.commit()

        payload = {
            "data": {
                "type": "customfield",
                "id": custom_field.id,
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
                f"{self.url}/{custom_field.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
