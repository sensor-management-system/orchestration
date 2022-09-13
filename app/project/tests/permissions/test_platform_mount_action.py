import datetime
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Configuration, Contact, PlatformMountAction, User
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
            begin_description="test mount platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            platform=platform,
        )
        platform_mount_action.configuration = configuration
        platform_mount_action.begin_contact = contact
        db.session.add_all(
            [platform, contact, user, configuration, platform_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(PlatformMountAction)
            .filter_by(id=platform_mount_action.id)
            .one()
        )
        self.assertEqual(
            action.begin_description, platform_mount_action.begin_description
        )
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
            begin_description="test mount internal platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            platform=platform,
        )
        platform_mount_action.configuration = configuration
        platform_mount_action.begin_contact = contact
        db.session.add_all(
            [platform, contact, user, configuration, platform_mount_action]
        )
        db.session.commit()
        action = (
            db.session.query(PlatformMountAction)
            .filter_by(id=platform_mount_action.id)
            .one()
        )
        self.assertEqual(
            action.begin_description, platform_mount_action.begin_description
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

    def test_mount_an_internal_platform(self):
        """Ensure mounting an internal platform works well."""
        platform = create_a_test_platform()
        parent_platform = create_a_test_platform()
        mock_jwt = generate_userinfo_data()
        contact = create_a_test_contact(mock_jwt)
        configuration = generate_configuration_model()
        # In order to make sure that we can create a platform mount
        # with a parent platform, we also must make sure that we
        # have an active mount for this parent platform.
        parent_platform_mount = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [platform, parent_platform, contact, configuration, parent_platform_mount]
        )
        db.session.commit()
        data = mount_payload_data(
            self.object_type, configuration, contact, parent_platform, platform
        )
        _ = super().add_object(
            url=f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
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
            begin_description="test mount public platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            platform=public_platform,
        )
        mount_public_platform.configuration = configuration
        mount_public_platform.begin_contact = contact

        mount_internal_platform = PlatformMountAction(
            begin_date=fake.date(),
            begin_description="test mount internal platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=user,
            platform=internal_platform,
        )
        mount_internal_platform.configuration = configuration
        mount_internal_platform.begin_contact = contact
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
        # a public platform.
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
                    f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
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
        parent_platform_mount = PlatformMountAction(
            configuration=configuration,
            platform=parent_platform,
            begin_contact=contact,
            begin_date=datetime.datetime(year=1970, month=1, day=1),
        )
        db.session.add_all(
            [
                platform,
                parent_platform,
                contact,
                configuration,
                parent_platform_mount,
            ]
        )
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
                    f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)

    def test_delete_action_as_a_group_member(self):
        """Ensure mounted platform groups can be deleted."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = create_a_test_platform(
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
            [platform, parent_platform, contact, configuration, parent_platform_mount1]
        )
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
                    f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
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

    def test_mount_a_platform_in_two_configuration_at_same_time(self):
        """Ensure mounting a platform in more than one configuration at the same time won't success."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = create_a_test_platform(
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
                platform,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
                parent_platform_mount1,
            ]
        )
        db.session.commit()
        # Mount a Platform Without unmount date
        data = mount_payload_data(
            self.object_type,
            first_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-04-05 00:21:34",
        )
        # Try to mount the previous platform at the same time but in another configuration.
        data_2 = mount_payload_data(
            self.object_type,
            second_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-04-05 00:21:34",
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)
            # This Should Fail as the Platform is active in a configuration.
            response_2 = self.client.post(
                f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                data=json.dumps(data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_2.status_code, 409)

    def test_mount_a_platform_with_time_interval_between_two_mount_actions(self):
        """
        Ensure mounting a platform between two mount actions if
        end_date M1 < Mount interval < begin_date of M2 will success.
        """
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = create_a_test_platform(
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
                platform,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
                parent_platform_mount1,
                parent_platform_mount2,
            ]
        )
        db.session.commit()
        # Mount a platform in this intervall ["2022-04-05 00:21:34", "2022-05-05 00:21:34"]
        data = mount_payload_data(
            self.object_type,
            first_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-04-05 00:21:34",
            end_date="2022-05-05 00:21:34",
        )
        # Mount the previous platform in this intervall ["2022-07-05 00:21:34", None]
        data_2 = mount_payload_data(
            self.object_type,
            second_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-07-05 00:21:34",
        )
        # Mount the previous platform in this intervall ["2022-06-05 00:21:34", "2022-06-28 00:21:34"]
        data_3 = mount_payload_data(
            self.object_type,
            second_configuration,
            contact,
            parent_platform,
            platform,
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
                    f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)
            # This should work as it there is no mount action after this one.
            response_2 = self.client.post(
                f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                data=json.dumps(data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_2.status_code, 201)
            # This should also work as it starts and end before the next mount action.
            response_3 = self.client.post(
                f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                data=json.dumps(data_3),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_3.status_code, 201)

    def test_mount_a_platform_with_time_interval_overlap_a_mount_actions(self):
        """
        Ensure mounting a platform between two mount actions if
        Mount interval overlap begin_date of M2 will Fail.
        """
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = create_a_test_platform(
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
                platform,
                parent_platform,
                contact,
                first_configuration,
                second_configuration,
                parent_platform_mount1,
                parent_platform_mount2,
            ]
        )
        db.session.commit()
        # Mount a platform in this intervall ["2022-04-05 00:21:34", "2022-05-05 00:21:34"]
        data = mount_payload_data(
            self.object_type,
            first_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-04-05 00:21:34",
            end_date="2022-05-05 00:21:34",
        )
        # Mount the previous platform in this intervall ["2022-07-05 00:21:34", None]
        data_2 = mount_payload_data(
            self.object_type,
            second_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-07-05 00:21:34",
        )
        # Mount the previous platform in this intervall ["2022-06-05 00:21:34", None]
        data_3 = mount_payload_data(
            self.object_type,
            second_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-06-05 00:21:34",
        )
        # Mount the previous platform in this intervall ["2022-06-05 00:21:34", "2022-08-05 00:21:34"]
        data_4 = mount_payload_data(
            self.object_type,
            second_configuration,
            contact,
            parent_platform,
            platform,
            begin_date="2022-06-05 00:21:34",
            end_date="2022-08-05 00:21:34",
        )
        # Mount the previous platform in this intervall ["2022-04-20 00:21:34", "2022-06-06 00:21:34"]
        data_5 = mount_payload_data(
            self.object_type,
            second_configuration,
            contact,
            parent_platform,
            platform,
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
                    f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 201)
            # This should work as it there is no mount action after this one.
            response_2 = self.client.post(
                f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                data=json.dumps(data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_2.status_code, 201)
            # This should not work as it there is no unmount date before the next mount action.
            response_3 = self.client.post(
                f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                data=json.dumps(data_3),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_3.status_code, 409)
            # This should not work as there is a conflict with the end_date.
            response_4 = self.client.post(
                f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                data=json.dumps(data_4),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_4.status_code, 409)
            # This should not work as there is a conflict with the begin_date.
            response_5 = self.client.post(
                f"{self.url}?include=platform,begin_contact,parent_platform,configuration",
                data=json.dumps(data_5),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_5.status_code, 409)


def mount_payload_data(
    object_type,
    configuration,
    contact,
    parent_platform,
    platform,
    begin_date=fake.future_datetime().__str__(),
    end_date=None,
):
    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "begin_description": "Test PlatformMountAction",
                "begin_date": begin_date,
                "end_date": end_date,
                "offset_x": str(fake.coordinate()),
                "offset_y": str(fake.coordinate()),
                "offset_z": str(fake.coordinate()),
            },
            "relationships": {
                "platform": {"data": {"type": "platform", "id": platform.id}},
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
