"""Tests for the Platform-Permissions."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Platform, User
from project.api.models.base_model import db
from project.api.models.idl_user import IdlUser
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.permissions import create_a_test_contact, create_superuser_token

IDL_USER_ACCOUNT = IdlUser(
    id="1000",
    username="testuser@ufz.de",
    administrated_permission_groups=["1"],
    membered_permission_groups=["2", "3"],
)


class TestPlatformPermissions(BaseTestCase):
    """Tests for the platform Permissions."""

    platform_url = base_url + "/platforms"
    object_type = "platform"

    def test_add_public_platform(self):
        """Ensure a new platform can be public."""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(public_platform)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=public_platform.id).one()
        self.assertEqual(platform.is_public, True)
        self.assertEqual(platform.is_internal, False)
        self.assertEqual(platform.is_private, False)

    def test_add_private_platform(self):
        """Ensure a new platform can be private."""
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
        )
        db.session.add(private_platform)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=private_platform.id).one()
        self.assertEqual(platform.is_public, False)
        self.assertEqual(platform.is_internal, False)
        self.assertEqual(platform.is_private, True)

    def test_add_internal_platform_model(self):
        """Ensure a new platform model can be internal."""
        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            is_internal=True,
            is_public=False,
            is_private=False,
        )
        db.session.add(internal_platform)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=internal_platform.id).one()
        self.assertEqual(platform.is_internal, True)
        self.assertEqual(platform.is_public, False)
        self.assertEqual(platform.is_private, False)

    def test_add_internal_platform(self):
        """Ensure a new platform can be added to api and is internal."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"]["attributes"]["is_internal"], True)
        self.assertEqual(data["data"]["attributes"]["is_public"], False)
        self.assertEqual(data["data"]["attributes"]["is_private"], False)

    def test_get_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            is_private=False,
            is_internal=False,
            is_public=True,
        )

        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            is_public=False,
            is_internal=False,
            is_private=True,
        )
        db.session.add_all([public_platform, internal_platform, private_platform])
        db.session.commit()

        response = self.client.get(self.platform_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["id"], str(public_platform.id))

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal, and only his own private objects"""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            is_public=False,
            is_internal=False,
            is_private=True,
        )
        private_platform_1 = Platform(
            id=3,
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
        )

        contact = create_a_test_contact()
        contact_1 = create_a_test_contact()

        user = User(subject="test_user@test.test", contact=contact)
        user_1 = User(subject="test_user1@test.test", contact=contact_1)
        db.session.add_all(
            [
                public_platform,
                internal_platform,
                private_platform,
                private_platform_1,
                contact,
                user,
                contact_1,
                user_1,
            ]
        )
        db.session.commit()

        private_platform.created_by_id = user.id
        private_platform_1.created_by_id = user_1.id

        token_data = {
            "sub": user.subject,
            "iss": "SMS unittest",
            "family_name": contact.family_name,
            "given_name": contact.given_name,
            "email": contact.email,
            "aud": "SMS",
        }
        access_headers = create_token(token_data)
        response = self.client.get(self.platform_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 3)

    def test_add_platform_with_multiple_permission_values(self):
        """Make sure that is a a platform can't have multiple True permission values at the same time"""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

        platform_data_1 = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data_1),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

        platform_data_2 = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_add_groups_ids(self):
        """Make sure that a platform with groups-ids can be created"""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                    "group_ids": ["12"],
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["data"]["attributes"]["group_ids"], ["12"])

    def test_get_an_internal_platforms_as_an_unregistered_user(self):
        """An unregistered user should not be able to
        retrieve an internal Platform."""

        internal_platform = Platform(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(internal_platform)
        db.session.commit()
        url = f"{self.platform_url}/{internal_platform.id}"
        response = self.client.get(url)
        self.assertNotEqual(response.status, 200)

    def test_get_an_private_platform_as_not_owner_user(self):
        """Make sure that a normal user is not allowed a retrieve a not owned
        private platform."""

        c = create_a_test_contact()
        user = User(subject="test_user1@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        private_platform = Platform(
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
            created_by_id=user.id,
        )
        db.session.add(private_platform)
        db.session.commit()

        access_headers = create_token()
        url = f"{self.platform_url}/{private_platform.id}"
        response = self.client.get(url, headers=access_headers)
        self.assertEqual(response.status, "403 FORBIDDEN")

    def test_get_an_private_platform_as_anonymous(self):
        """Make sure that a normal user is not allowed a retrieve a
        private platform."""

        c = create_a_test_contact()
        user = User(subject="test_user1@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        private_platform = Platform(
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
            created_by_id=user.id,
        )
        db.session.add(private_platform)
        db.session.commit()

        url = f"{self.platform_url}/{private_platform.id}"
        response = self.client.get(url)
        self.assertEqual(response.status, "401 UNAUTHORIZED")

    def test_patch_platform_as_a_member_in_a_permission_group(self):
        """Make sure that a member in a group (admin/member) can change
        the platform data per patch request"""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        for platform_data in platforms:
            with self.client:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["group_ids"],
            )
            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                platform_data_changed = {
                    "data": {
                        "type": "platform",
                        "id": data["data"]["id"],
                        "attributes": {"short_name": "Changed platform name"},
                    }
                }
                url = f"{self.platform_url}/{data['data']['id']}"
                res = super().update_object(
                    url, platform_data_changed, self.object_type
                )
                self.assertEqual(
                    res["data"]["attributes"]["short_name"],
                    platform_data_changed["data"]["attributes"]["short_name"],
                )

    def test_patch_platform_user_not_in_any_permission_group(self):
        """Make sure that a user can only do changes in platforms, where he/she is involved."""
        group_id_test_user_is_not_included = ["13"]
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_not_included
        )
        access_headers = create_token()
        for platform_data in platforms:
            with self.client:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["group_ids"],
                group_id_test_user_is_not_included,
            )
            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:

                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                platform_data_changed = {
                    "data": {
                        "type": "platform",
                        "id": data["data"]["id"],
                        "attributes": {"short_name": "Forbidden"},
                    }
                }
                url = f"{self.platform_url}/{data['data']['id']}"
                access_headers = create_token()
                with self.client:
                    response = self.client.patch(
                        url,
                        data=json.dumps(platform_data_changed),
                        content_type="application/vnd.api+json",
                        headers=access_headers,
                    )
                self.assertEqual(response.status, "403 FORBIDDEN")

    def test_delete_platform_access_forbidden(self):
        """Make sure that only admins can delete a platform in the same permission group."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        for platform_data in platforms:
            with self.client:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["group_ids"],
            )
            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:

                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                url = f"{self.platform_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                delete_data = json.loads(delete_response.data.decode())
                self.assertEqual(delete_data["errors"][0]["status"], 403)

    def test_delete_platform_as_an_admin_in_a_permission_group(self):
        """Make sure that a permission group admins are allowed to delete a platform."""
        group_id_test_user_is_member_in_1 = (
            IDL_USER_ACCOUNT.administrated_permission_groups
        )
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_member_in_1
        )
        access_headers = create_token()
        for platform_data in platforms:
            with self.client:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["group_ids"],
                group_id_test_user_is_member_in_1,
            )

            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:

                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                url = f"{self.platform_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                self.assertEqual(delete_response.status_code, 200)

    def test_delete_private_platform_as_superuser(self):
        """Make sure that a superuser is allowed to delete not owned private platforms"""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": False,
                    "is_private": True,
                },
            }
        }
        access_headers = create_superuser_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT

            url = f"{self.platform_url}/{data['data']['id']}"
            delete_response = self.client.delete(url, headers=access_headers)
            self.assertEqual(delete_response.status_code, 200)

    def test_delete_platform_as_superuser_not_involved_in_permission_group(self):
        """Make sure that a superuser can delete a platform even if he/she is not admin in
        the corresponding permission group."""
        group_id_test_user_is_not_included = ["40"]
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_not_included
        )
        access_headers = create_superuser_token()
        for platform_data in platforms:
            with self.client:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["group_ids"],
                group_id_test_user_is_not_included,
            )

            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:

                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                url = f"{self.platform_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                self.assertEqual(delete_response.status_code, 200)


def preparation_of_public_and_internal_platform_data(group_ids):
    """
    Data to add an internal and a public platform.

    :param group_ids: list of permission groups
    :return: list of data for two platforms [public, internal]
    """
    public_platform_data = {
        "data": {
            "type": "platform",
            "attributes": {
                "short_name": fake.pystr(),
                "is_public": True,
                "is_internal": False,
                "is_private": False,
                "group_ids": group_ids,
            },
        }
    }
    internal_platform_data = {
        "data": {
            "type": "platform",
            "attributes": {
                "short_name": fake.pystr(),
                "is_public": False,
                "is_internal": True,
                "is_private": False,
                "group_ids": group_ids,
            },
        }
    }
    platforms = [public_platform_data, internal_platform_data]
    return platforms
