# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the configurations-relationships."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Configuration
from project.api.models.base_model import db
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token
from project.tests.permissions import create_a_test_contact
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def create_a_test_configuration(public=False, internal=True, cfg_permission_group=None):
    public_config = Configuration(
        label="public configuration",
        is_public=public,
        is_internal=internal,
        cfg_permission_group=cfg_permission_group,
    )
    db.session.add(public_config)
    db.session.commit()
    return public_config


class TestDeviceRelationshipPermissions(BaseTestCase):
    """Tests for the Configuration relationship Permissions."""

    def test_fail_adding_relationship_to_configurations_without_jwt(self):
        """Ensure adding a relationship without a valid token will fail."""
        public_config = create_a_test_configuration(
            public=True,
            internal=False,
        )
        contact = create_a_test_contact()
        db.session.add_all([public_config, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/configurations/{public_config.id}/relationships/contacts"
        with self.client:
            response = self.client.post(
                url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 401)

    def test_fail_adding_relationship_to_configurations_with_no_group(self):
        """Ensure adding a relationship to a no group configurations will success."""
        public_config = create_a_test_configuration(
            public=True,
            internal=False,
        )
        contact = create_a_test_contact()
        db.session.add_all([public_config, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/configurations/{public_config.id}/relationships/contacts"
        with self.client:
            response = self.client.post(
                url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 403)

    def test_fail_adding_relationship_to_configurations_with_a_group_other_than_user(
        self,
    ):
        """Ensure adding a relationship will fail if user not involve in parent permission group."""
        public_config = create_a_test_configuration(
            public=True, internal=False, cfg_permission_group="403"
        )
        contact = create_a_test_contact()
        db.session.add_all([public_config, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/configurations/{public_config.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_success_adding_relationship_to_configurations_with_a_group(self):
        """Ensure adding a relationship will success if user in parent permission group."""
        public_config = create_a_test_configuration(
            public=True,
            internal=False,
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0],
        )
        contact = create_a_test_contact()
        db.session.add_all([public_config, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/configurations/{public_config.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_fail_updating_relationship_to_configurations_with_a_group_other_than_user(
        self,
    ):
        """Ensure updating a relationship will fail if user not involve in parent permission group."""
        public_config = create_a_test_configuration(
            public=True,
            internal=False,
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0],
        )
        contact = create_a_test_contact()
        contact_2 = create_a_test_contact()
        db.session.add_all([public_config, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        data_2 = {"data": [{"type": "contact", "id": contact_2.id}]}
        url = base_url + f"/configurations/{public_config.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response.status_code, 200)

                public_config.cfg_permission_group = "403"
                response_patch = self.client.patch(
                    url,
                    data=json.dumps(data_2),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response_patch.status_code, 403)

    def test_success_updating_relationship_to_configurations_with_a_group_other_than_user(
        self,
    ):
        """Ensure updating a relationship will fail if user not involve in parent permission group."""
        public_config = create_a_test_configuration(
            public=True,
            internal=False,
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0],
        )
        contact = create_a_test_contact()
        contact_2 = create_a_test_contact()
        db.session.add_all([public_config, contact])
        db.session.commit()

        data = {"data": [{"type": "contact", "id": contact.id}]}
        data_2 = {"data": [{"type": "contact", "id": contact_2.id}]}
        url = base_url + f"/configurations/{public_config.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response.status_code, 200)

                response_patch = self.client.patch(
                    url,
                    data=json.dumps(data_2),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                self.assertEqual(response_patch.status_code, 200)

    def test_fail_delete_a_relationship_to_configurations_with_a_group_other_than_user(
        self,
    ):
        """Ensure Deletion fails if user not in parent permission group."""
        contact = create_a_test_contact()
        public_config = Configuration(
            label="test",
            is_public=True,
            is_internal=False,
            cfg_permission_group="403",
            contacts=[contact],
        )

        db.session.add_all([public_config, contact])
        db.session.commit()
        data = {"data": [{"type": "contact", "id": contact.id}]}
        url = base_url + f"/configurations/{public_config.id}/relationships/contacts"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)
