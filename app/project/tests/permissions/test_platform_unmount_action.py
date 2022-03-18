import json
from unittest.mock import patch

from project import base_url
from project.api.models import Configuration
from project.api.models import Contact, User
from project.api.models import Platform
from project.api.models import PlatformMountAction
from project.api.models import PlatformUnmountAction
from project.api.models.base_model import db
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_userinfo_data, create_token
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.permissions import create_a_test_platform, create_a_test_contact
from project.tests.permissions.platform_mount_action import mount_payload_data
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def platform_unmount_action_model(public=True, private=False, internal=False):
    platform = Platform(
        short_name="Test platform",
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
    platform_mount_action = PlatformMountAction(
        begin_date=fake.date(),
        description="test mount internal platform action model",
        offset_x=fake.coordinate(),
        offset_y=fake.coordinate(),
        offset_z=fake.coordinate(),
        created_by=user,
        platform=platform,
    )
    platform_mount_action.configuration = configuration
    platform_mount_action.contact = contact
    platform_unmount_action = PlatformUnmountAction(
        end_date=fake.date(),
        description="test unmount platform action model",
        created_by=user,
        platform=platform,
    )
    platform_unmount_action.configuration = configuration
    platform_unmount_action.contact = contact
    db.session.add_all(
        [
            platform,
            contact,
            user,
            configuration,
            platform_mount_action,
            platform_unmount_action,
        ]
    )
    db.session.commit()
    action = (
        db.session.query(PlatformUnmountAction)
        .filter_by(id=platform_unmount_action.id)
        .one()
    )
    return action, platform_unmount_action


class TestMountPlatformPermissions(BaseTestCase):
    """Tests for the Unmount Platform Permissions."""

    mount_url = base_url + "/platform-mount-actions"
    unmount_url = base_url + "/platform-unmount-actions"
    object_type = "platform_unmount_action"

    def test_unmount_a_public_platform(self):
        """Ensure unmounting a public platform will be listed."""
        action, platform_unmount_action = platform_unmount_action_model()
        self.assertEqual(action.description, platform_unmount_action.description)
        response = self.client.get(self.unmount_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_unmount_an_internal_platform_model(self):
        """Ensure unmounting an internal platform won't be listed unless user provide a valid JWT."""
        action, platform_unmount_action = platform_unmount_action_model(
            public=False, private=False, internal=True
        )
        self.assertEqual(action.description, platform_unmount_action.description)

        # Without a valid JWT -> Will not be listed.
        response = self.client.get(self.unmount_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.unmount_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_unmount_a_device_with_permission_group(self):
        """Ensure unmounting with a permission group will success."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = create_a_test_platform(group_ids=group_id_test_user_is_member_in_2,)
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        db.session.add_all(
            [
                platform,
                parent_platform,
                contact,
                configuration,
            ]
        )
        db.session.commit()
        mount_data = mount_payload_data(
            "platform_mount_action",
            configuration,
            contact,
            platform,
            parent_platform,
            begin_date="2022-02-18 20:44:42",
        )
        unmount_data = payload_unmount_data(contact, platform, configuration)

        access_headers = create_token()
        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                mount_response = self.client.post(
                    f"{self.mount_url}?include=platform,contact,parent_platform,configuration",
                    data=json.dumps(mount_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(mount_response.status_code, 201)

                unmount_response = self.client.post(
                    f"{self.unmount_url}?include=platform,contact,configuration",
                    data=json.dumps(unmount_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                self.assertEqual(unmount_response.status_code, 201)


def payload_unmount_data(contact, platform, first_configuration):
    unmount_data = {
        "data": {
            "type": "platform_unmount_action",
            "attributes": {
                "description": "test unmount platform action",
                "end_date": "2022-02-28 20:44:42",
            },
            "relationships": {
                "platform": {"data": {"type": "platform", "id": platform.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
                "configuration": {
                    "data": {"type": "configuration", "id": first_configuration.id}
                },
            },
        }
    }
    return unmount_data
