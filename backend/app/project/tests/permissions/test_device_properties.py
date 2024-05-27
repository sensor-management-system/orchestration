# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the device property endpoints."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Device, DeviceProperty, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions.test_customfields import create_a_test_device
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def device_properties_model(public=True, private=False, internal=False, group_ids=None):
    """Create and return entities for 2 devies & 3 device properties."""
    device1 = Device(
        short_name=fake.pystr(),
        manufacturer_name=fake.company(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    device2 = Device(
        short_name=fake.pystr(),
        manufacturer_name=fake.company(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    db.session.add(device1)
    db.session.add(device2)
    db.session.commit()
    device_property1 = DeviceProperty(
        label="device property1",
        property_name="device_property1",
        device=device1,
    )
    device_property2 = DeviceProperty(
        label="device property2",
        property_name="device_property2",
        device=device1,
    )
    device_property3 = DeviceProperty(
        label="device property3",
        property_name="device_property3",
        device=device2,
    )
    db.session.add_all([device_property1, device_property2, device_property3])
    db.session.commit()
    return device1, device2, device_property1, device_property2, device_property3


class TestDevicePropertyServices(BaseTestCase):
    """Test device properties."""

    url = base_url + "/device-properties"

    def test_get_public_device_property_api(self):
        """Ensure that we can get a list of public device properties."""
        _ = device_properties_model()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_device_property_api(self):
        """Ensure that we can get a list of internal device properties with a valid jwt."""
        _ = device_properties_model(public=False, private=False, internal=True)

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
            self.assertEqual(len(response.json["data"]), 3)

    def test_post_device_property_api(self):
        """Ensure that we can add a device property."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(device.id is not None)

        count_device_properties = (
            db.session.query(DeviceProperty)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        self.assertEqual(count_device_properties, 0)
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device_property1",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                },
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
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 201)
        device_properties = query_result_to_list(
            db.session.query(DeviceProperty).filter_by(
                device_id=device.id,
            )
        )
        self.assertEqual(len(device_properties), 1)

        device_property = device_properties[0]
        self.assertEqual(device_property.label, "device property1")
        self.assertEqual(device_property.compartment_name, "climate")
        self.assertEqual(device_property.sampling_media_name, "air")
        self.assertEqual(device_property.device_id, device.id)
        self.assertEqual(
            str(device_property.device_id), response.get_json()["data"]["id"]
        )

    def test_post_device_property_for_archived_device(self):
        """Ensure that we can' add for an archived device."""
        device = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        device.archived = True
        db.session.add(device)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device_property1",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                },
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
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_device_property_api(self):
        """Ensure that we can update a device property."""
        device1 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        device2 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)

        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device1,
        )
        db.session.add(device_property1)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {
                    "label": "property 2",
                    "property_name": "device_property2",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url_patch = base_url + "/device-properties/" + str(device_property1.id)
                response = self.client.patch(
                    url_patch,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 200)

        device_property_reloaded = (
            db.session.query(DeviceProperty).filter_by(id=device_property1.id).one()
        )
        self.assertEqual(device_property_reloaded.label, "property 2")
        self.assertEqual(device_property_reloaded.device_id, device2.id)

    def test_patch_device_property_for_archived_source_device(self):
        """Ensure we can't update a device property for an archived device."""
        device1 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        device2 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)

        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device1,
        )
        device1.archived = True
        db.session.add_all([device_property1, device1])
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {
                    "label": "property 2",
                    "property_name": "device_property2",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url_patch = base_url + "/device-properties/" + str(device_property1.id)
                response = self.client.patch(
                    url_patch,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 403)

    def test_patch_device_property_for_archived_target_device(self):
        """Ensure we can't update a device property for an archived target device."""
        device1 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)
        device2 = create_a_test_device(IDL_USER_ACCOUNT.membered_permission_groups)

        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device1,
        )
        device2.archived = True
        db.session.add_all([device_property1, device2])
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {
                    "label": "property 2",
                    "property_name": "device_property2",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url_patch = base_url + "/device-properties/" + str(device_property1.id)
                response = self.client.patch(
                    url_patch,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 403)

    def test_delete_device_property_api(self):
        """Ensure that we can delete a device property."""
        device = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        db.session.add_all([device, device_property])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    self.url + "/" + str(device_property.id),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

            self.assertEqual(response.status_code, 200)
        device_reloaded = db.session.query(Device).filter_by(id=device.id).first()
        msg = "delete;measured quantity"
        self.assertEqual(msg, device_reloaded.update_description)

    def test_delete_device_property_for_archived_device(self):
        """Ensure that we can't delete a device property for an archived device."""
        device = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups,
            archived=True,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        db.session.add_all([device, device_property])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    self.url + "/" + str(device_property.id),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 403)

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
        dv_property = DeviceProperty(
            device=device1,
            property_name="Temp",
            property_uri="something",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([device1, device2, contact, user, dv_property])
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": dv_property.id,
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
                        f"{self.url}/{dv_property.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
