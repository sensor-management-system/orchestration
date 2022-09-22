"""Tests for the devices."""
import datetime
import json
from unittest.mock import patch

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    PlatformMountAction,
    User,
)
from project.api.models.base_model import db
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.permissions import (
    create_a_test_contact,
    create_a_test_device,
    create_a_test_platform,
)
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def payload_data(
    object_type,
    configuration,
    contact,
    device,
    parent_platform,
    begin_date=None,
    end_date=None,
):
    """Create some example payload to create device mounts."""
    if not begin_date:
        begin_date = fake.future_datetime().__str__()
    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "begin_description": "Test DeviceMountAction",
                "begin_date": begin_date,
                "end_date": end_date,
                "offset_x": str(fake.coordinate()),
                "offset_y": str(fake.coordinate()),
                "offset_z": str(fake.coordinate()),
            },
            "relationships": {
                "device": {"data": {"type": "device", "id": device.id}},
                "begin_contact": {"data": {"type": "contact", "id": contact.id}},
                "parent_platform": {
                    "data": {"type": "platform", "id": parent_platform.id}
                },
                "configuration": {
                    "data": {"type": "configuration", "id": configuration.id}
                },
            },
        }
    }
    return data


class TestMountDevicePermissions(BaseTestCase):
    """Tests for the Mount Device Permissions."""

    url = base_url + "/device-mount-actions"
    unmount_url = base_url + "/device-unmount-actions"
    object_type = "device_mount_action"

    def test_mount_a_public_device(self):
        """Ensure mounting a public device works well."""
        device = create_a_test_device(public=True, internal=False)
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )
        device_mount_action = DeviceMountAction(
            begin_date=fake.date(),
            begin_description="test mount device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            device=device,
        )
        device_mount_action.parent_platform = parent_platform
        device_mount_action.configuration = configuration
        device_mount_action.begin_contact = contact
        db.session.add_all(
            [device, parent_platform, contact, user, configuration, device_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(DeviceMountAction)
            .filter_by(id=device_mount_action.id)
            .one()
        )
        self.assertEqual(
            action.begin_description, device_mount_action.begin_description
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_mount_an_internal_device_model(self):
        """Ensure mounting an internal device as model works well."""
        device = create_a_test_device()
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )
        device_mount_action = DeviceMountAction(
            begin_date=fake.date(),
            begin_description="test mount internal device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            device=device,
        )
        device_mount_action.parent_platform = parent_platform
        device_mount_action.configuration = configuration
        device_mount_action.begin_contact = contact
        db.session.add_all(
            [device, parent_platform, contact, user, configuration, device_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(DeviceMountAction)
            .filter_by(id=device_mount_action.id)
            .one()
        )
        self.assertEqual(
            action.begin_description, device_mount_action.begin_description
        )

        # Without a valid JWT -> Will not be listed.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_mount_an_internal_device(self):
        """Ensure mounting an internal device works well."""
        device = create_a_test_device()
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        _ = super().add_object(
            url=f"{self.url}?include=device,begin_contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal."""
        public_device = Device(
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        internal_device = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )

        mount_public_device = DeviceMountAction(
            begin_date=fake.date(),
            begin_description="test mount public device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            device=public_device,
        )
        mount_public_device.configuration = configuration
        mount_public_device.begin_contact = contact
        mount_internal_device = DeviceMountAction(
            begin_date=fake.date(),
            begin_description="test mount internal device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            device=internal_device,
        )
        mount_internal_device.configuration = configuration
        mount_internal_device.begin_contact = contact

        db.session.add_all(
            [
                public_device,
                internal_device,
                contact,
                user,
                configuration,
                mount_public_device,
                mount_internal_device,
            ]
        )
        db.session.commit()
        token_data = {
            "sub": user.subject,
            "iss": "SMS unittest",
            "family_name": contact.family_name,
            "given_name": contact.given_name,
            "email": contact.email,
            "aud": "SMS",
        }
        # Without JWT -> Should provide only actions related to
        # a public device.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 1)

        # With a valid JWT.
        access_headers = create_token(token_data)
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 2)

    def test_post_action_as_not_a_group_member(self):
        """Ensure mounting a device in a group fails if not done by member of group."""
        device = create_a_test_device(
            group_ids=[222],
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        db.session.add_all([device, parent_platform, contact, configuration])
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 403)

    def test_post_action_as_a_group_member(self):
        """Ensure mounting a device in a group succeeds if done by group member."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)

    def test_post_action_for_archived_device(self):
        """Ensure we can't mount an archived device."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        device.archived = True
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 409)

    def test_post_action_for_archived_configuration(self):
        """Ensure we can't mount on an archived configuration."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        configuration.archived = True
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 409)

    def test_post_action_for_archived_parent_platform(self):
        """Ensure we can't mount on an archived parent platform."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        parent_platform.archived = True
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 409)

    def test_delete_action_as_a_group_member(self):
        """Ensure mounted device groups can be deleted."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                url = f"{self.url}/{data['data']['id']}"
                delete_response_user_is_a_member = self.client.delete(
                    url, headers=access_headers
                )
                self.assertEqual(delete_response_user_is_a_member.status_code, 200)

    def test_delete_for_archived_device(self):
        """Ensure we can't delete the device mount for an archived device."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                url = f"{self.url}/{data['data']['id']}"
                device.archived = True
                db.session.add(device)
                db.session.commit()

                delete_response_user_is_a_member = self.client.delete(
                    url, headers=access_headers
                )
                self.assertEqual(delete_response_user_is_a_member.status_code, 409)

    def test_delete_for_archived_configuration(self):
        """Ensure we can't delete the device mount for an archived configuration."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                url = f"{self.url}/{data['data']['id']}"
                configuration.archived = True
                db.session.add(configuration)
                db.session.commit()

                delete_response_user_is_a_member = self.client.delete(
                    url, headers=access_headers
                )
                self.assertEqual(delete_response_user_is_a_member.status_code, 409)

    def test_delete_for_archived_parent_platform(self):
        """Ensure we can't delete the device mount for an archived parent platform."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                url = f"{self.url}/{data['data']['id']}"
                parent_platform.archived = True
                db.session.add(configuration)
                db.session.commit()

                delete_response_user_is_a_member = self.client.delete(
                    url, headers=access_headers
                )
                self.assertEqual(delete_response_user_is_a_member.status_code, 409)

    def test_mount_a_device_in_two_configuration_at_different_time(self):
        """Ensure mounting a device in > 1 configurations at the different time will succeed."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        first_configuration = generate_configuration_model()
        second_configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=first_configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=2022, month=1, day=1),
        )
        db.session.add_all(
            [
                device,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
                parent_platform_mount1,
            ]
        )
        db.session.commit()
        mount_data = payload_data(
            self.object_type,
            first_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-02-18 20:44:42",
        )
        mount_data["data"]["attributes"]["end_date"] = "2022-02-28 20:44:42"
        mount_data["data"]["attributes"][
            "end_description"
        ] = "test unmount device action"
        mount_data["data"]["relationships"]["end_contact"] = {
            "data": {"type": "contact", "id": contact.id}
        }
        mount_data_2 = payload_data(
            self.object_type,
            first_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-03-18 20:44:42",
        )

        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                mount_response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(mount_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(mount_response.status_code, 201)

                mount_response_2 = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(mount_data_2),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(mount_response_2.status_code, 201)

    def test_mount_a_device_in_two_configuration_at_same_time(self):
        """Ensure mounting devices in > 1 configuration at the same time won't success."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        first_configuration = generate_configuration_model()
        second_configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=first_configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=2022, month=4, day=5),
        )
        db.session.add_all(
            [
                device,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
                parent_platform_mount1,
            ]
        )
        db.session.commit()
        # Mount a Device Without unmount date
        data = payload_data(
            self.object_type,
            first_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-04-05 00:21:34",
        )
        # Try to mount the previous device at the same time but in another configuration.
        data_2 = payload_data(
            self.object_type,
            second_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-04-05 00:21:34",
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)
            # This Should Fail as the Device is active in a configuration.
            response_2 = self.client.post(
                f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                data=json.dumps(data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_2.status_code, 409)

    def test_mount_a_device_with_time_interval_between_two_mount_actions(self):
        """
        Check that we can add two mount actions if they don't overlap.

        Ensure mounting a device between two mount actions if
        end_date M1 < Mount interval < begin_date of M2 will succeed.
        """
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        first_configuration = generate_configuration_model()
        second_configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=first_configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=2022, month=4, day=5),
            end_date=datetime.datetime(year=2022, month=5, day=6),
        )
        parent_platform_mount2 = PlatformMountAction(
            configuration=second_configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=2022, month=6, day=1),
        )
        db.session.add_all(
            [
                device,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
                parent_platform_mount1,
                parent_platform_mount2,
            ]
        )
        db.session.commit()
        # Mount a device in this interval
        # ["2022-04-05 00:21:34", "2022-05-05 00:21:34"]
        data = payload_data(
            self.object_type,
            first_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-04-05 00:21:34",
            end_date="2022-05-05 00:21:34",
        )
        # Mount the previous device in this interval
        # ["2022-07-05 00:21:34", None]
        data_2 = payload_data(
            self.object_type,
            second_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-07-05 00:21:34",
        )
        # Mount the previous device in this interval
        # ["2022-06-05 00:21:34", "2022-06-28 00:21:34"]
        data_3 = payload_data(
            self.object_type,
            second_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-06-05 00:21:34",
            end_date="2022-06-28 00:21:34",
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)
            # This should work as it there is no mount action after this one.
            response_2 = self.client.post(
                f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                data=json.dumps(data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_2.status_code, 201)
            # This should also work as it starts and end before the next mount action.
            response_3 = self.client.post(
                f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                data=json.dumps(data_3),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_3.status_code, 201)

    def test_mount_a_device_with_time_interval_overlap_a_mount_actions(self):
        """
        Ensure we don't alow overlapping mounts.

        Ensure mounting a device between two mount actions if
        Mount interval overlap begin_date of M2 will Fail.
        """
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        first_configuration = generate_configuration_model()
        second_configuration = generate_configuration_model()
        # In order to make sure that we can create a platform mount
        # with a parent platform, we also must make sure that we
        # have an active mount for this parent platform.
        parent_platform_mount1 = PlatformMountAction(
            configuration=first_configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=2022, month=4, day=5),
            end_date=datetime.datetime(year=2022, month=5, day=6),
        )
        parent_platform_mount2 = PlatformMountAction(
            configuration=second_configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=2022, month=7, day=5),
        )
        db.session.add_all(
            [
                device,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
                parent_platform_mount1,
                parent_platform_mount2,
            ]
        )
        db.session.commit()
        # Mount a device in this intervall ["2022-04-05 00:21:34", "2022-05-05 00:21:34"]
        data = payload_data(
            self.object_type,
            first_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-04-05 00:21:34",
            end_date="2022-05-05 00:21:34",
        )
        # Mount the previous device in this intervall ["2022-07-05 00:21:34", None]
        data_2 = payload_data(
            self.object_type,
            second_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-07-05 00:21:34",
        )
        # Mount the previous device in this intervall ["2022-06-05 00:21:34", None]
        data_3 = payload_data(
            self.object_type,
            second_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-06-05 00:21:34",
        )
        # Mount the previous device in this interval
        # ["2022-06-05 00:21:34", "2022-08-05 00:21:34"]
        data_4 = payload_data(
            self.object_type,
            second_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-06-05 00:21:34",
            end_date="2022-08-05 00:21:34",
        )
        # Mount the previous device in this interval
        # ["2022-04-20 00:21:34", "2022-06-06 00:21:34"]
        data_5 = payload_data(
            self.object_type,
            second_configuration,
            contact,
            device,
            parent_platform,
            begin_date="2022-04-20 00:21:34",
            end_date="2022-06-06 00:21:34",
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)
            # This should work as it there is no mount action after this one.
            response_2 = self.client.post(
                f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                data=json.dumps(data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_2.status_code, 201)
            # This should not work as it there is no unmount date before the next mount action.
            response_3 = self.client.post(
                f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                data=json.dumps(data_3),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_3.status_code, 409)
            # This should not work as there is a conflict with the end_date.
            response_4 = self.client.post(
                f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                data=json.dumps(data_4),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_4.status_code, 409)
            # This should not work as there is a conflict with the begin_date.
            response_5 = self.client.post(
                f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                data=json.dumps(data_5),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_5.status_code, 409)

    def test_patch_for_archived_device(self):
        """Ensure we can't patch the device mount for an archived device."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                url = f"{self.url}/{data['data']['id']}"
                device.archived = True
                db.session.add(device)
                db.session.commit()

                payload = {
                    "data": {
                        "type": "device_mount_action",
                        "id": str(data["data"]["id"]),
                        "attributes": {"begin_description": "some new description"},
                    }
                }
                patch_response_user_is_a_member = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    headers=access_headers,
                    content_type="application/vnd.api+json",
                )
                self.assertEqual(patch_response_user_is_a_member.status_code, 409)

    def test_patch_for_archived_configuration(self):
        """Ensure we can't patch the device mount for an archived configuration."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                url = f"{self.url}/{data['data']['id']}"
                configuration.archived = True
                db.session.add(configuration)
                db.session.commit()

                payload = {
                    "data": {
                        "type": "device_mount_action",
                        "id": str(data["data"]["id"]),
                        "attributes": {"begin_description": "some new description"},
                    }
                }
                patch_response_user_is_a_member = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    headers=access_headers,
                    content_type="application/vnd.api+json",
                )
                self.assertEqual(patch_response_user_is_a_member.status_code, 409)

    def test_patch_for_archived_parent_platform(self):
        """Ensure we can't patch the device mount for an archived parent platform."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        device = create_a_test_device(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        parent_platform_mount1 = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [device, parent_platform, contact, configuration, parent_platform_mount1]
        )
        db.session.commit()
        data = payload_data(
            self.object_type, configuration, contact, device, parent_platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(response.status_code, 201)
                data = json.loads(response.data.decode())
                url = f"{self.url}/{data['data']['id']}"
                parent_platform.archived = True
                db.session.add(configuration)
                db.session.commit()

                payload = {
                    "data": {
                        "type": "device_mount_action",
                        "id": str(data["data"]["id"]),
                        "attributes": {"begin_description": "some new description"},
                    }
                }
                patch_response_user_is_a_member = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    headers=access_headers,
                    content_type="application/vnd.api+json",
                )
                self.assertEqual(patch_response_user_is_a_member.status_code, 409)
