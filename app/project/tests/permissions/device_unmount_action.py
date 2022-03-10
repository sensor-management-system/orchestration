"""Tests for the devices."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Configuration
from project.api.models import Device, Platform, Contact
from project.api.models import DeviceMountAction
from project.api.models import DeviceUnmountAction
from project.api.models import User
from project.api.models.base_model import db
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_userinfo_data, create_token
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.permissions import create_a_test_contact
from project.tests.permissions import (
    create_a_test_platform,
    create_a_test_device,
)
from project.tests.permissions.device_mount_action import payload_data
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def device_unmount_action_model(public=True, private=False, internal=False):
    device = Device(
        short_name=fake.pystr(),
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    parent_platform = Platform(
        short_name="device parent platform",
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    mock_jwt = generate_userinfo_data()
    contact = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    user = User(subject=mock_jwt["sub"], contact=contact)
    configuration = Configuration(
        label=fake.pystr(), is_public=public, is_internal=internal,
    )
    device_mount_action = DeviceMountAction(
        begin_date=fake.date(),
        description="test mount device action model",
        offset_x=fake.coordinate(),
        offset_y=fake.coordinate(),
        offset_z=fake.coordinate(),
        created_by=user,
        device=device,
    )
    device_mount_action.parent_platform = parent_platform
    device_mount_action.configuration = configuration
    device_mount_action.contact = contact
    unmount_device_action = DeviceUnmountAction(
        end_date=fake.date(),
        description="test unmount device action model",
        created_by=user,
        device=device,
    )
    unmount_device_action.configuration = configuration
    unmount_device_action.contact = contact
    db.session.add_all(
        [
            device,
            parent_platform,
            contact,
            user,
            configuration,
            device_mount_action,
            unmount_device_action,
        ]
    )
    db.session.commit()
    action = (
        db.session.query(DeviceUnmountAction)
        .filter_by(id=unmount_device_action.id)
        .one()
    )
    return action, unmount_device_action


class TestUnmountDevicePermissions(BaseTestCase):
    """Tests for the Mount Device Permissions."""

    mount_url = base_url + "/device-mount-actions"
    unmount_url = base_url + "/device-unmount-actions"
    object_type = "device_unmount_action"

    def test_unmount_a_public_device(self):
        """Ensure unmounting a public device will be listed."""
        action, unmount_device_action = device_unmount_action_model()
        self.assertEqual(action.description, unmount_device_action.description)
        response = self.client.get(self.unmount_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_unmount_an_internal_device(self):
        """Ensure unmounting an internal device won't be listed unless user provide a valid JWT."""
        action, unmount_device_action = device_unmount_action_model(
            public=False, private=False, internal=True
        )
        self.assertEqual(action.description, unmount_device_action.description)
        response = self.client.get(self.unmount_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.unmount_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_mount_a_device_in_two_configuration_at_different_time(self):
        """Ensure mounting a device in more than one configuration at the different time will success."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(group_ids=group_id_test_user_is_member_in_2,)
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        first_configuration = generate_configuration_model()
        second_configuration = generate_configuration_model()
        db.session.add_all(
            [
                device,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
            ]
        )
        db.session.commit()
        mount_data = payload_data(
            "device_mount_action",
            first_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-02-18 20:44:42",
        )
        unmount_data = payload_unmount_data(contact, device, first_configuration)

        access_headers = create_token()
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                mount_response = self.client.post(
                    f"{self.mount_url}?include=device,contact,parent_platform,configuration",
                    data=json.dumps(mount_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(mount_response.status_code, 201)

                unmount_response = self.client.post(
                    f"{self.unmount_url}?include=device,contact,configuration",
                    data=json.dumps(unmount_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(unmount_response.status_code, 201)


def payload_unmount_data(contact, device, first_configuration):
    unmount_data = {
        "data": {
            "type": "device_unmount_action",
            "attributes": {
                "description": "test unmount device action",
                "end_date": "2022-02-28 20:44:42",
            },
            "relationships": {
                "device": {"data": {"type": "device", "id": device.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
                "configuration": {
                    "data": {"type": "configuration", "id": first_configuration.id}
                },
            },
        }
    }
    return unmount_data
