# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the Configuration-Permissions."""
import json

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.permissions import create_a_test_contact, create_superuser_token


class TestConfigurationPermissions(BaseTestCase):
    """Tests for the configuration Permissions."""

    configuration_url = base_url + "/configurations"
    object_type = "configuration"

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
        db.session.add_all([contact, normal_contact, self.normal_user, self.super_user])
        db.session.commit()

    def test_add_public_configuration(self):
        """Ensure a new configuration can be public."""
        public_config = Configuration(
            id=15,
            label="public configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(public_config)
        db.session.commit()

        configuration = (
            db.session.query(Configuration).filter_by(id=public_config.id).one()
        )
        self.assertEqual(configuration.is_public, True)
        self.assertEqual(configuration.is_internal, False)

    def test_add_configuration_model(self):
        """Ensure a new configuration model can be internal."""
        internal_config = Configuration(
            id=33,
            label="internal configuration",
            is_internal=True,
            is_public=False,
        )
        db.session.add(internal_config)
        db.session.commit()

        configuration = (
            db.session.query(Configuration).filter_by(id=internal_config.id).one()
        )
        self.assertEqual(configuration.is_internal, True)
        self.assertEqual(configuration.is_public, False)

    def test_add_configuration(self):
        """Ensure a new configuration can be added to api and is internal."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()

        configuration_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "cfg_permission_group": str(permission_group.id),
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            with self.client:
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"]["attributes"]["is_internal"], True)
        self.assertEqual(data["data"]["attributes"]["is_public"], False)

    def test_get_all_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_config = Configuration(
            id=15, label=fake.pystr(), is_internal=False, is_public=True
        )

        internal_config = Configuration(
            id=33, label=fake.pystr(), is_public=False, is_internal=True
        )

        db.session.add_all([public_config, internal_config])
        db.session.commit()

        response = self.client.get(self.configuration_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["id"], str(public_config.id))

    def test_get_an_internal_config_as_anonymous_user(self):
        """Ensure anonymous user can't access an internal configuration."""
        internal_config = Configuration(
            label=fake.pystr(), is_public=False, is_internal=True
        )

        db.session.add(internal_config)
        db.session.commit()
        url = f"{self.configuration_url}/{internal_config.id}"
        response = self.client.get(url)
        self.assertNotEqual(response.status, 200)

    def test_get_as_registered_user(self):
        """Ensure a registered user can see public, internal, and only his own private objects."""
        public_config = Configuration(
            id=15,
            label=fake.pystr(),
            is_public=True,
            is_internal=False,
        )

        internal_config = Configuration(
            id=33,
            label=fake.pystr(),
            is_public=False,
            is_internal=True,
        )

        contact = create_a_test_contact()
        contact_1 = create_a_test_contact()

        user = User(subject="test_user@test.test", contact=contact)
        user_1 = User(subject="test_user1@test.test", contact=contact_1)
        db.session.add_all(
            [public_config, internal_config, contact, user, contact_1, user_1]
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
        access_headers = create_token(token_data)
        response = self.client.get(self.configuration_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 2)

    def test_add_configuration_with_multiple_true_visibility_values(self):
        """Ensure a configuration can't have multiple True visibility values at the same time."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()
        configuration_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "cfg_permission_group": str(permission_group.id),
                },
            }
        }
        with self.run_requests_as(self.super_user):
            with self.client:
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 409)

    def test_add_group_ids(self):
        """Ensure that a configuration with group ids can be created."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()
        config_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "cfg_permission_group": str(permission_group.id),
                },
            }
        }
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(config_data),
                content_type="application/vnd.api+json",
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            data["data"]["attributes"]["cfg_permission_group"],
            str(permission_group.id),
        )

    def test_patch_configuration_as_a_member_in_a_permission_group(self):
        """Ensure a member in a group can change the configuration."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()

        group_id_test_user_is_member_in_2 = str(permission_group.id)
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_member_in_2
        )
        for configuration_data in configs:
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["cfg_permission_group"],
            )
            configuration_data_changed = {
                "data": {
                    "type": "configuration",
                    "id": data["data"]["id"],
                    "attributes": {"label": "Changed configuration name"},
                }
            }
            url = f"{self.configuration_url}/{data['data']['id']}"
            with self.run_requests_as(self.normal_user):
                res = super().update_object(
                    url, configuration_data_changed, self.object_type
                )
            self.assertEqual(
                res["data"]["attributes"]["label"],
                configuration_data_changed["data"]["attributes"]["label"],
            )

    def test_patch_archived_configuration(self):
        """Make sure we can't patch an archived configuration."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()

        group_id_test_user_is_member_in_2 = str(permission_group.id)

        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_member_in_2
        )
        for configuration_data in configs:
            with self.client:
                with self.run_requests_as(self.super_user):
                    response = self.client.post(
                        self.configuration_url,
                        data=json.dumps(configuration_data),
                        content_type="application/vnd.api+json",
                    )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["cfg_permission_group"],
            )

            configuration = (
                db.session.query(Configuration).filter_by(id=data["data"]["id"]).first()
            )
            configuration.archived = True
            db.session.add(configuration)
            db.session.commit()
            configuration_data_changed = {
                "data": {
                    "type": "configuration",
                    "id": data["data"]["id"],
                    "attributes": {"label": "Changed configuration name"},
                }
            }
            url = f"{self.configuration_url}/{data['data']['id']}"
            with self.run_requests_as(self.normal_user):
                _ = super().try_update_object_with_status_code(
                    url, configuration_data_changed, expected_status_code=403
                )

    def test_patch_configuration_user_not_in_any_permission_group(self):
        """Ensure a user can only do changes in configurations, where he/she is involved."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        db.session.add_all([permission_group])
        db.session.commit()

        group_id_test_user_is_not_included = str(permission_group.id)

        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_not_included
        )
        for configuration_data in configs:
            with self.run_requests_as(self.super_user):
                response = self.client.post(
                    self.configuration_url,
                    data=json.dumps(configuration_data),
                    content_type="application/vnd.api+json",
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["cfg_permission_group"],
                group_id_test_user_is_not_included,
            )
            configuration_data_changed_forbidden = {
                "data": {
                    "type": "configuration",
                    "id": data["data"]["id"],
                    "attributes": {"label": "Forbidden"},
                }
            }
            url = f"{self.configuration_url}/{data['data']['id']}"
            with self.run_requests_as(self.normal_user):
                with self.client:
                    response = self.client.patch(
                        url,
                        data=json.dumps(configuration_data_changed_forbidden),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status, "403 FORBIDDEN")

    def test_patch_configuration_no_permission_group_set(self):
        """Ensure a user can change a configuration if cfg_permission_group is not set."""
        configs = preparation_of_public_and_internal_configuration_data()
        access_headers = create_token()
        for configuration_data in configs:
            configuration = Configuration(**configuration_data["data"]["attributes"])
            db.session.add(configuration)
            db.session.commit()

            configuration_data_changed = {
                "data": {
                    "type": "configuration",
                    "id": configuration.id,
                    "attributes": {"label": "Changed"},
                }
            }
            url = f"{self.configuration_url}/{configuration.id}"
            access_headers = create_token()
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(configuration_data_changed),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status, "200 OK")

    def test_delete_configuration_as_member_in_a_permission_group(self):
        """Make sure that a group member can't delete a configuration."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=self.normal_user
        )
        db.session.add_all([permission_group, membership])
        db.session.commit()
        group_id_test_user_is_member_in_2 = str(permission_group.id)
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_member_in_2
        )
        for configuration_data in configs:
            with self.run_requests_as(self.super_user):
                with self.client:
                    response = self.client.post(
                        self.configuration_url,
                        data=json.dumps(configuration_data),
                        content_type="application/vnd.api+json",
                    )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["cfg_permission_group"],
            )
            url = f"{self.configuration_url}/{data['data']['id']}"
            with self.run_requests_as(self.normal_user):
                delete_response = self.client.delete(
                    url,
                )
                self.assertEqual(delete_response.status_code, 403)

    def test_delete_configuration_as_super_user(self):
        """Ensure a superuser can delete a configuration even if not member in permission groups."""
        group_id_test_user_is_not_included = "20"
        configs = preparation_of_public_and_internal_configuration_data(
            group_id_test_user_is_not_included
        )
        access_headers = create_superuser_token()
        for configuration_data in configs:
            with self.client:
                with self.run_requests_as(self.super_user):
                    response = self.client.post(
                        self.configuration_url,
                        data=json.dumps(configuration_data),
                        content_type="application/vnd.api+json",
                    )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(
                data["data"]["attributes"]["cfg_permission_group"],
                group_id_test_user_is_not_included,
            )

            url = f"{self.configuration_url}/{data['data']['id']}"
            with self.run_requests_as(self.super_user):
                delete_response = self.client.delete(url, headers=access_headers)
            self.assertEqual(delete_response.status_code, 200)

    def test_patch_to_different_permission_group(self):
        """Ensure we can't update to a permission group we aren't members."""
        permission_group = PermissionGroup(name="test", entitlement="test")
        other_group = PermissionGroup(name="other", entitlement="other")
        db.session.add_all([permission_group, other_group])
        db.session.commit()

        configuration = Configuration(
            label="Dummy config",
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(permission_group.id),
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        membership = PermissionGroupMembership(
            permission_group=permission_group, user=user
        )
        db.session.add_all([configuration, contact, user, membership])
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration",
                "id": configuration.id,
                "attributes": {"cfg_permission_group": str(other_group.id)},
                "relationships": {},
            }
        }

        with self.run_requests_as(user):
            response = self.client.patch(
                f"{self.configuration_url}/{configuration.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_config_with_pid_as_superuser(self):
        """Make sure that even a superuser can't delete a configuration with pid."""
        configuration_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": True,
                    "is_internal": False,
                    "cfg_permission_group": "40",
                    "persistent_identifier": "pid0-0000-0001-1234",
                },
            }
        }
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(configuration_data),
                content_type="application/vnd.api+json",
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        url = f"{self.configuration_url}/{data['data']['id']}"
        with self.run_requests_as(self.super_user):
            delete_response = self.client.delete(url)
        # Due to the pid, we can't delete it anymore
        self.assertEqual(delete_response.status_code, 403)


def preparation_of_public_and_internal_configuration_data(group_id=None):
    """
    Prepare data to add an internal and a public configuration.

    :param group_id: one permission group
    :return: list of data for two configs [public, internal]
    """
    public_configuration_data = {
        "data": {
            "type": "configuration",
            "attributes": {
                "label": fake.pystr(),
                "is_public": True,
                "is_internal": False,
            },
        }
    }
    internal_configuration_data = {
        "data": {
            "type": "configuration",
            "attributes": {
                "label": fake.pystr(),
                "is_public": False,
                "is_internal": True,
            },
        }
    }
    if group_id is not None:
        public_configuration_data["data"]["attributes"][
            "cfg_permission_group"
        ] = group_id
        internal_configuration_data["data"]["attributes"][
            "cfg_permission_group"
        ] = group_id

    configs = [public_configuration_data, internal_configuration_data]
    return configs
