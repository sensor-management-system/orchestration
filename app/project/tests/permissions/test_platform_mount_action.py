import json
from unittest.mock import patch

from project import base_url
from project.api.models import Configuration, PlatformMountAction, User
from project.api.models.base_model import db
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.permissions import create_a_test_contact, create_a_test_platform
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestMountPlatformPermissions(BaseTestCase):
    """Tests for the Mount Platform Permissions."""

    url = base_url + "/platform-mount-actions"
    object_type = "platform_mount_action"

    def test_mount_a_public_platform(self):
        """Ensure mounting a public platform works well."""
        platform = create_a_test_platform(public=True, internal=False)
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )
        platform_mount_action = PlatformMountAction(
            begin_date=fake.date(),
            description="test mount platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            platform=platform,
        )
        platform_mount_action.configuration = configuration
        platform_mount_action.contact = contact
        db.session.add_all(
            [platform, contact, user, configuration, platform_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(PlatformMountAction)
            .filter_by(id=platform_mount_action.id)
            .one()
        )
        self.assertEqual(action.description, platform_mount_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_mount_an_internal_platform_model(self):
        """Ensure mounting an internal platform as model works well."""
        platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
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
        db.session.add_all(
            [platform, contact, user, configuration, platform_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(PlatformMountAction)
            .filter_by(id=platform_mount_action.id)
            .one()
        )
        self.assertEqual(action.description, platform_mount_action.description)

        # Without a valid JWT -> Will not be listed.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_mount_an_internal_platform(self):
        """Ensure mounting an internal device works well."""
        platform = create_a_test_platform()
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        db.session.add_all([platform, parent_platform, contact, configuration])
        db.session.commit()
        data = mount_payload_data(
            self.object_type, configuration, contact, parent_platform, platform
        )
        _ = super().add_object(
            url=f"{self.url}?include=platform,contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal."""

        public_platform = create_a_test_platform(
            public=True,
            private=False,
            internal=False,
        )
        internal_platform = create_a_test_platform(
            public=False,
            private=False,
            internal=True,
        )
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        user = User(subject=mock_jwt["sub"], contact=contact)
        configuration = Configuration(
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )
        mount_public_platform = PlatformMountAction(
            begin_date=fake.date(),
            description="test mount public device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            platform=public_platform,
        )
        mount_public_platform.configuration = configuration
        mount_public_platform.contact = contact

        mount_internal_platform = PlatformMountAction(
            begin_date=fake.date(),
            description="test mount internal device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            platform=internal_platform,
        )
        mount_internal_platform.configuration = configuration
        mount_internal_platform.contact = contact
        db.session.add_all(
            [
                public_platform,
                internal_platform,
                contact,
                user,
                configuration,
                mount_public_platform,
                mount_internal_platform,
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
        """Ensure mounting a platform in a group fails
        if it mounted as someone not member in the group."""
        platform = create_a_test_platform(
            group_ids=[222],
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        db.session.add_all([platform, parent_platform, contact, configuration])
        db.session.commit()
        data = mount_payload_data(
            self.object_type, configuration, contact, parent_platform, platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=platform,contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 403)

    def test_post_action_as_a_group_member(self):
        """Ensure mounting a platform in a group success
        if it mounted from a group member."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = create_a_test_platform(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        db.session.add_all([platform, parent_platform, contact, configuration])
        db.session.commit()
        data = mount_payload_data(
            self.object_type, configuration, contact, parent_platform, platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=platform,contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)

    def test_delete_action_as_a_group_member(self):
        """Ensure mounted device groups can be deleted."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = create_a_test_platform(
            group_ids=group_id_test_user_is_member_in_2,
        )
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        db.session.add_all([platform, parent_platform, contact, configuration])
        db.session.commit()
        data = mount_payload_data(
            self.object_type, configuration, contact, parent_platform, platform
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=platform,contact,parent_platform,configuration",
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


def mount_payload_data(
    object_type,
    configuration,
    contact,
    parent_platform,
    platform,
    begin_date=fake.future_datetime().__str__(),
):
    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": "Test PlatformMountAction",
                "begin_date": begin_date,
                "offset_x": str(fake.coordinate()),
                "offset_y": str(fake.coordinate()),
                "offset_z": str(fake.coordinate()),
            },
            "relationships": {
                "platform": {"data": {"type": "platform", "id": platform.id}},
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
    return data
