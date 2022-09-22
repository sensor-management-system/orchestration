"""Tests for the generic configuration actions api."""
import json
from datetime import datetime
from unittest.mock import patch

from project import base_url, db
from project.api.models import Configuration, GenericConfigurationAction
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.models.test_generic_actions_models import (
    generate_configuration_action_model,
)
from project.tests.permissions import create_a_test_configuration, create_a_test_contact
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def make_generic_configuration_action_data(object_type, cfg_permission_group=None):
    """
    Create the json payload for a generic configuration action.

    This also creates some associated objects in the database.
    """
    configuration = create_a_test_configuration(cfg_permission_group)
    contact = create_a_test_contact()

    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": fake.paragraph(nb_sentences=3),
                "action_type_name": fake.lexify(
                    text="Random type: ??????????", letters="ABCDE"
                ),
                "action_type_uri": fake.uri(),
                "begin_date": datetime.now().__str__(),
            },
            "relationships": {
                "configuration": {
                    "data": {"type": "configuration", "id": configuration.id}
                },
                "contact": {"data": {"type": "contact", "id": contact.id}},
            },
        }
    }
    return data


class TestGenericConfigurationActionPermissions(BaseTestCase):
    """Tests for the GenericConfigurationAction permissions."""

    url = base_url + "/generic-configuration-actions"
    object_type = "generic_configuration_action"

    def test_a_public_generic_configuration_action(self):
        """Ensure a public generic configuration action will be listed."""
        generic_configuration_action = generate_configuration_action_model(
            is_public=True, is_internal=False
        )
        action = (
            db.session.query(GenericConfigurationAction)
            .filter_by(id=generic_configuration_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_configuration_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_a_internal_generic_configuration_action(self):
        """Ensure an internal generic configuration action won't be listed for anonymous."""
        generic_configuration_action = generate_configuration_action_model(
            is_public=False, is_internal=True
        )
        action = (
            db.session.query(GenericConfigurationAction)
            .filter_by(id=generic_configuration_action.id)
            .one()
        )
        self.assertEqual(action.description, generic_configuration_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_add_generic_configuration_action_with_a_permission_group(self):
        """Ensure POST a new generic configuration action can be added to the database."""
        payload = make_generic_configuration_action_data(
            self.object_type,
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0],
        )
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 201)

    def test_post_for_archived_configuration(self):
        """Ensure POST a new generic configuration action can be added to the database."""
        payload = make_generic_configuration_action_data(
            self.object_type,
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0],
        )
        configuration = db.session.query(Configuration).order_by("created_at").first()
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()

        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 409)

    def test_post_generic_configuration_action_data_user_not_in_the_permission_group(
        self,
    ):
        """Post to configuration,with permission Group different from the user group."""
        payload = make_generic_configuration_action_data(
            self.object_type, cfg_permission_group=403
        )
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_action_with_a_permission_group(self):
        """Post to generic_configuration_action_data,with permission Group."""
        payload = generate_configuration_action_model(
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0]
        )
        self.assertTrue(payload.id is not None)
        generic_configuration_action_updated = {
            "data": {
                "type": self.object_type,
                "id": payload.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{payload.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(generic_configuration_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_patch_for_archived_configuration(self):
        """Ensure that we can't patch for archived configurations."""
        payload = generate_configuration_action_model(
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0]
        )
        configuration = db.session.query(Configuration).order_by("created_at").first()
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()

        generic_configuration_action_updated = {
            "data": {
                "type": self.object_type,
                "id": payload.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{payload.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(generic_configuration_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 409)

    def test_patch_generic_configuration_action_data_user_is_not_part_from_permission_group(
        self,
    ):
        """Post to configuration,with permission Group."""
        generic_configuration_action = generate_configuration_action_model(
            cfg_permission_group=403
        )
        self.assertTrue(generic_configuration_action.id is not None)
        generic_configuration_action_updated = {
            "data": {
                "type": self.object_type,
                "id": generic_configuration_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{generic_configuration_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(generic_configuration_action_updated),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_generic_configuration_action_data(self):
        """Delete generic_configuration_action_data."""
        generic_configuration_action = generate_configuration_action_model(
            cfg_permission_group=IDL_USER_ACCOUNT.administrated_permission_groups[0]
        )
        url = f"{self.url}/{generic_configuration_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_configuration(self):
        """Ensure we can't delete for archived configurations."""
        generic_configuration_action = generate_configuration_action_model(
            cfg_permission_group=IDL_USER_ACCOUNT.administrated_permission_groups[0]
        )
        configuration = db.session.query(Configuration).order_by("created_at").first()
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()
        url = f"{self.url}/{generic_configuration_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 409)

    def test_delete_generic_configuration_action_data_as_member(self):
        """Delete generic_configuration_action_data as member."""
        generic_configuration_action = generate_configuration_action_model(
            cfg_permission_group=IDL_USER_ACCOUNT.membered_permission_groups[0]
        )
        url = f"{self.url}/{generic_configuration_action.id}"
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)
