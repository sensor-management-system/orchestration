# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the Platform-Permissions."""
import json

from project import base_url
from project.api.models import (
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    Platform,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.permissions import (
    create_a_test_contact,
    create_a_test_platform,
    create_superuser_token,
)


class TestPlatformPermissions(BaseTestCase):
    """Tests for the platform Permissions."""

    platform_url = base_url + "/platforms"
    object_type = "platform"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)
        contact = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.super_user = User(
            subject=contact.email, contact=contact, is_superuser=True
        )

        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                contact,
                normal_contact,
                self.normal_user,
                self.super_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_add_public_platform(self):
        """Ensure a new platform can be public."""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
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
            manufacturer_name=fake.company(),
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
            manufacturer_name=fake.company(),
            is_internal=True,
            is_public=False,
            is_private=False,
            group_ids=["12"],
        )
        db.session.add(internal_platform)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=internal_platform.id).one()
        self.assertEqual(platform.is_internal, True)
        self.assertEqual(platform.is_public, False)
        self.assertEqual(platform.is_private, False)

    def test_add_internal_platform(self):
        """Ensure a new platform can be added to api and is internal."""
        group_id_test_user_is_member_in_2 = [str(self.permission_group.id)]
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                    "group_ids": group_id_test_user_is_member_in_2,
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
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
            manufacturer_name=fake.company(),
            is_private=False,
            is_internal=False,
            is_public=True,
        )

        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
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
        """Ensure a registered user can see public, internal, and only his own private objects."""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_internal=False,
            is_private=True,
        )
        private_platform_1 = Platform(
            id=3,
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
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
        """Ensure that a platform can't have multiple True permission values at the same time."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": False,
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
        self.assertEqual(response.status_code, 409)

        platform_data_1 = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
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
                    "manufacturer_name": fake.company(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_add_groups_ids(self):
        """Make sure that a platform with groups ids can be created."""
        group_id_test_user_is_member_in_2 = [str(self.permission_group.id)]
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                    "group_ids": group_id_test_user_is_member_in_2,
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            data["data"]["attributes"]["group_ids"], group_id_test_user_is_member_in_2
        )

    def test_get_an_internal_platforms_as_an_unregistered_user(self):
        """An unregistered user should not be able to view an internal Platform."""
        internal_platform = Platform(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
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
        """Make sure that a normal user is not allowed a view not owned private platforms."""
        c = create_a_test_contact()
        user = User(subject="test_user1@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        private_platform = Platform(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
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
        """Make sure that a anonymous user is not allowed to view private platforms."""
        c = create_a_test_contact()
        user = User(subject="test_user1@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        private_platform = Platform(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=True,
            is_internal=False,
            created_by_id=user.id,
        )
        db.session.add(private_platform)
        db.session.commit()

        url = f"{self.platform_url}/{private_platform.id}"
        response = self.client.get(url)
        self.assertIn(response.status_code, [401, 403])

    def test_patch_platform_as_a_member_in_a_permission_group(self):
        """Make sure that a member in a group (admin/member) can patch a platform."""
        group_id_test_user_is_member_in_2 = [str(self.permission_group.id)]
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_member_in_2
        )
        with self.run_requests_as(self.normal_user):
            for platform_data in platforms:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                )

                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)

                self.assertIn(
                    group_id_test_user_is_member_in_2[0],
                    data["data"]["attributes"]["group_ids"],
                )

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

    def test_patch_archived_platform(self):
        """Make sure that we can't patch an archived platform."""
        group_id_test_user_is_member_in_2 = [str(self.permission_group.id)]
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_member_in_2
        )
        with self.run_requests_as(self.normal_user):
            for platform_data in platforms:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                )

                data = json.loads(response.data.decode())

                self.assertEqual(response.status_code, 201)

                self.assertIn(
                    group_id_test_user_is_member_in_2[0],
                    data["data"]["attributes"]["group_ids"],
                )
                platform = (
                    db.session.query(Platform).filter_by(id=data["data"]["id"]).first()
                )
                platform.archived = True
                db.session.add(platform)
                db.session.commit()

                platform_data_changed = {
                    "data": {
                        "type": "platform",
                        "id": data["data"]["id"],
                        "attributes": {"short_name": "Changed platform name"},
                    }
                }
                url = f"{self.platform_url}/{data['data']['id']}"
                _ = super().try_update_object_with_status_code(
                    url, platform_data_changed, expected_status_code=403
                )

    def test_patch_platform_user_not_in_any_permission_group(self):
        """Make sure that a user can only do changes in platforms, where he/she is involved."""
        public_platform = create_a_test_platform(
            public=True,
            private=False,
            internal=False,
            group_ids=[str(self.other_group.id)],
        )

        db.session.add(public_platform)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            platform_data_changed = {
                "data": {
                    "type": "platform",
                    "id": public_platform.id,
                    "attributes": {"short_name": "Forbidden"},
                }
            }
            url = f"{self.platform_url}/{public_platform.id}"
            response = self.client.patch(
                url,
                data=json.dumps(platform_data_changed),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status, "403 FORBIDDEN")

    def test_delete_platform_access_forbidden(self):
        """Make sure that a member in a permission group can't delete the platform."""
        group_id_test_user_is_member_in_2 = [str(self.permission_group.id)]
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_member_in_2
        )

        with self.run_requests_as(self.normal_user):
            for platform_data in platforms:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                )

                data = json.loads(response.data.decode())

                self.assertEqual(response.status_code, 201)

                self.assertIn(
                    group_id_test_user_is_member_in_2[0],
                    data["data"]["attributes"]["group_ids"],
                )
                url = f"{self.platform_url}/{data['data']['id']}"
                delete_response = self.client.delete(url)
                delete_data = json.loads(delete_response.data.decode())
                self.assertEqual(delete_data["errors"][0]["status"], 403)

    def test_delete_private_platform_as_superuser(self):
        """Make sure that a superuser is allowed to delete not owned private platforms."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": False,
                    "is_private": True,
                },
            }
        }
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        with self.run_requests_as(self.super_user):
            url = f"{self.platform_url}/{data['data']['id']}"
            delete_response = self.client.delete(url)
        self.assertEqual(delete_response.status_code, 200)

    def test_delete_platform_as_superuser_not_involved_in_permission_group(self):
        """
        Make sure that a superuser can delete a platform.

        It doesn't matter if the superuser is part of a group or not.
        """
        group_id_test_user_is_not_included = [str(self.other_group.id)]
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_not_included
        )
        with self.run_requests_as(self.super_user):
            for platform_data in platforms:
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                )

                data = json.loads(response.data.decode())

                self.assertEqual(response.status_code, 201)

                self.assertEqual(
                    data["data"]["attributes"]["group_ids"],
                    group_id_test_user_is_not_included,
                )

                url = f"{self.platform_url}/{data['data']['id']}"
                delete_response = self.client.delete(url)
                self.assertEqual(delete_response.status_code, 200)

    def test_delete_platform_with_pid_as_superuser(self):
        """Make sure that even a superuser can't delete a platform with pid."""
        group_id_test_user_is_not_included = [str(self.other_group.id)]
        platforms = preparation_of_public_and_internal_platform_data(
            group_id_test_user_is_not_included
        )
        for idx, platform_data in enumerate(platforms):
            # Make sure that we set a pid
            platform_data["data"]["attributes"][
                "persistent_identifier"
            ] = platform_data["data"]["attributes"]["short_name"] + str(idx)
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    self.platform_url,
                    data=json.dumps(platform_data),
                    content_type="application/vnd.api+json",
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["group_ids"],
                group_id_test_user_is_not_included,
            )

            with self.run_requests_as(self.super_user):
                url = f"{self.platform_url}/{data['data']['id']}"
                delete_response = self.client.delete(url)
            self.assertEqual(delete_response.status_code, 403)

    def test_add_internal_platform_without_group(self):
        """Ensure a new internal platfrom can't be added without a group."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_add_public_platform_without_group(self):
        """Ensure a new public platform can't be added without a group."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": True,
                    "is_internal": False,
                    "is_private": False,
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_add_private_platform_without_group(self):
        """Ensure a new private platform can be added without a group."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": False,
                    "is_private": True,
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 201)

    def test_patch_to_different_permission_group(self):
        """Ensure we can't update to a permission group we aren't members."""
        platform = Platform(
            short_name="test platform",
            is_public=False,
            is_internal=True,
            group_ids=[str(self.permission_group.id)],
        )
        db.session.add_all(
            [
                platform,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "platform",
                "id": platform.id,
                "attributes": {
                    "group_ids": [str(self.other_group.id)],
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.platform_url}/{platform.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_remove_permission_group_non_admin(self):
        """Ensure we can't remove a permission group we aren't member."""
        platform = Platform(
            short_name="test platform",
            is_public=False,
            is_internal=True,
            group_ids=[str(self.permission_group.id), str(self.other_group.id)],
        )
        db.session.add_all([platform])
        db.session.commit()

        payload = {
            "data": {
                "type": "platform",
                "id": platform.id,
                "attributes": {
                    "group_ids": [str(self.permission_group.id)],
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.platform_url}/{platform.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_from_internal_to_private(self):
        """Ensure we can't set back to private once the platform was visible."""
        platform = Platform(
            short_name="test platform",
            is_public=False,
            is_internal=True,
            group_ids=[str(self.permission_group.id)],
        )
        db.session.add_all([platform])
        db.session.commit()

        payload = {
            "data": {
                "type": "platform",
                "id": platform.id,
                "attributes": {
                    "group_ids": [],
                    "is_private": True,
                    "is_internal": False,
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.platform_url}/{platform.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)


def preparation_of_public_and_internal_platform_data(group_ids):
    """
    Prepare data to add an internal and a public platform.

    :param group_ids: list of permission groups
    :return: list of data for two platforms [public, internal]
    """
    public_platform_data = {
        "data": {
            "type": "platform",
            "attributes": {
                "short_name": fake.pystr(),
                "manufacturer_name": fake.company(),
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
                "manufacturer_name": fake.company(),
                "is_public": False,
                "is_internal": True,
                "is_private": False,
                "group_ids": group_ids,
            },
        }
    }
    platforms = [public_platform_data, internal_platform_data]
    return platforms
