"""Tests for the devices."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Configuration
from project.api.models import Contact, User, Device
from project.api.models import DeviceMountAction
from project.api.models import Platform
from project.api.models.base_model import db
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_token_data, create_token
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestDevicePermissions(BaseTestCase):
    """Tests for the Device Permissions."""

    url = base_url + "/device-mount-actions"
    object_type = "device_mount_action"

    def test_mount_a_public_device(self):
        """Test """
        device = Device(
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parent_platform = Platform(
            short_name="device parent platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(), is_public=True, is_internal=False,
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
        db.session.add_all(
            [device, parent_platform, contact, user, configuration, device_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(DeviceMountAction)
            .filter_by(id=device_mount_action.id)
            .one()
        )
        self.assertEqual(action.description, device_mount_action.description)

    def test_mount_an_internal_device_model(self):
        device = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        parent_platform = Platform(
            short_name="device parent platform",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(), is_public=True, is_internal=False,
        )
        device_mount_action = DeviceMountAction(
            begin_date=fake.date(),
            description="test mount internal device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            device=device,
        )
        device_mount_action.parent_platform = parent_platform
        device_mount_action.configuration = configuration
        device_mount_action.contact = contact
        db.session.add_all(
            [device, parent_platform, contact, user, configuration, device_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(DeviceMountAction)
            .filter_by(id=device_mount_action.id)
            .one()
        )
        self.assertEqual(action.description, device_mount_action.description)

    def test_mount_an_internal_device(self):
        device = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        parent_platform = Platform(
            short_name="device parent platform",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = Configuration(
            label=fake.pystr(), is_public=True, is_internal=False,
        )
        db.session.add_all([device, parent_platform, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test DeviceMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device,contact,parent_platform,configuration",
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
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(), is_public=True, is_internal=False,
        )
        mount_public_device = DeviceMountAction(
            begin_date=fake.date(),
            description="test mount public device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            device=public_device,
        )
        mount_public_device.configuration = configuration
        mount_public_device.contact = contact

        mount_internal_device = DeviceMountAction(
            begin_date=fake.date(),
            description="test mount internal device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            device=internal_device,
        )
        mount_internal_device.configuration = configuration
        mount_internal_device.contact = contact
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
        # Test without token. Should provide only actions related to
        # a public device.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 1)

        # Test with token.
        access_headers = create_token(token_data)
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 2)

    def test_add_groups_ids_as_not_group_member(self):
        """Make sure that a device with groups-ids fails if it mounted an not members."""
        device = Device(
            short_name=fake.linux_processor(),
            is_public=True,
            is_private=False,
            is_internal=False,
            group_ids=[222],
        )
        parent_platform = Platform(
            short_name="device parent platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = generate_configuration_model()
        db.session.add_all([device, parent_platform, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test DeviceMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                f"{self.url}?include=device,contact,parent_platform,configuration",
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 403)

    def test_add_groups_ids_as_a_group_member(self):
        """Make sure that a device with groups-ids success if it mounted from a group member."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permissions_groups
        device = Device(
            short_name=fake.linux_processor(),
            is_public=True,
            is_private=False,
            is_internal=False,
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = Platform(
            short_name="device parent platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = generate_configuration_model()
        db.session.add_all([device, parent_platform, contact, configuration])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test DeviceMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            Idl, "get_all_permission_groups"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=device,contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)
