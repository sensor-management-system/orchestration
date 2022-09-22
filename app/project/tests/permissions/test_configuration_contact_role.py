"""Tests for the configuration contact roles with permission management."""

import json
from unittest.mock import patch

from project import base_url, db
from project.api.models import Configuration, ConfigurationContactRole, Contact, User
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, generate_userinfo_data
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def generate_configuration(
    public=True,
    internal=False,
    group_id=None,
):
    """Generate a configuration to work with."""
    if not group_id:
        group_id = []
    configuration = Configuration(
        label="short_name test",
        is_public=public,
        is_internal=internal,
        cfg_permission_group=group_id,
    )
    db.session.add(configuration)
    db.session.commit()
    return configuration


def generate_contact():
    """Generate a contact to work with."""
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add(contact)
    db.session.commit()
    return contact


def generate_configuration_contact_role(
    public=True,
    internal=False,
    group_id=None,
):
    """Generate a configuration contact role to work with."""
    configuration = generate_configuration(
        public=public, internal=internal, group_id=group_id
    )
    contact = generate_contact()
    configuration_contact_role = ConfigurationContactRole(
        configuration=configuration,
        contact=contact,
        role_name="Operator",
        role_uri="https://server/cv/api/v1/contactroles/3",
    )
    db.session.add(configuration_contact_role)
    db.session.commit()
    return configuration_contact_role


class TestConfigurationContactRolePermissions(BaseTestCase):
    """Tests for the configuration contact roles."""

    url = base_url + "/configuration-contact-roles"
    object_type = "configuration_contact_role"

    def test_getlist_public_configuration_contact_role(self):
        """Ensure that a contact role for a public configuration will be listed."""
        configuration_contact_role = generate_configuration_contact_role()
        role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role.id)
            .one()
        )
        self.assertEqual(role.role_name, configuration_contact_role.role_name)
        self.assertEqual(role.role_uri, configuration_contact_role.role_uri)
        self.assertEqual(role.configuration, configuration_contact_role.configuration)
        self.assertEqual(
            role.configuration.is_public,
            configuration_contact_role.configuration.is_public,
        )
        self.assertEqual(role.configuration.is_public, True)
        self.assertEqual(role.contact, configuration_contact_role.contact)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"][0]["id"], str(role.id))

    def test_getlist_internal_configuration_contact_role_anonymous(self):
        """Ensure that a contact role for an internal configuration is not listed for anonymous."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role.id)
            .one()
        )

        self.assertEqual(
            role.configuration.is_internal,
            configuration_contact_role.configuration.is_internal,
        )
        self.assertEqual(role.configuration.is_internal, True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_getlist_interal_configuration_contact_role_logged_in(self):
        """Ensure that contact role for an internal configuration is listed for logged in users."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role.id)
            .one()
        )

        self.assertEqual(
            role.configuration.is_internal,
            configuration_contact_role.configuration.is_internal,
        )
        self.assertEqual(role.configuration.is_internal, True)

        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"][0]["id"], str(role.id))

    def test_getone_public_configuration_contact_role(self):
        """Ensure that a public contact role can be listed."""
        configuration_contact_role = generate_configuration_contact_role()
        role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role.id)
            .one()
        )
        response = self.client.get(self.url + f"/{role.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(role.id))

    def test_getone_internal_configuration_contact_role_anonymous(self):
        """Ensure that contact role for internal configuration is not accessble for anonymous."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role.id)
            .one()
        )
        response = self.client.get(self.url + f"/{role.id}")
        self.assertEqual(response.status_code, 401)

    def test_getone_interal_configuration_contact_role_logged_in(self):
        """Ensure that contact role for an internal configuration is listed for logged in users."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role.id)
            .one()
        )
        access_headers = create_token()
        response = self.client.get(self.url + f"/{role.id}", headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(role.id))

    def test_delete_public_configuration_contact_role_anonymous(self):
        """Ensure that a public contact role can't be deleted from anymous."""
        configuration_contact_role = generate_configuration_contact_role()
        response = self.client.delete(self.url + f"/{configuration_contact_role.id}")
        self.assertEqual(response.status_code, 401)

    def test_delete_public_configuration_contact_role_logged_in(self):
        """Ensure that contact role for public configuration can be deleted when no group_id."""
        configuration_contact_role = generate_configuration_contact_role()
        access_headers = create_token()
        response = self.client.delete(
            self.url + f"/{configuration_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_public_configuration_contact_role_member_in_group(self):
        """Ensure that contact role for public configuration can be deleted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="2")
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_archived_configuration(self):
        """Ensure we can't delete for an archived configuration."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="2")
        configuration_contact_role.configuration.archived = True
        db.session.add(configuration_contact_role.configuration)
        db.session.commit()

        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 409)

    def test_delete_public_configuration_contact_role_admin_in_group(self):
        """Ensure that contact role for public configuration can be deleted by admin of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="1")
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_public_configuration_contact_role_not_in_group(self):
        """Ensure contact role for public configuration can't be deleted by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="4")
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_public_configuration_contact_role_superuser(self):
        """Ensure that contact role for public configuration can still be deleted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="4")
        contact = configuration_contact_role.contact
        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )
        db.session.add_all([other_contact, admin_user])
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_configuration_contact_role_anonymous(self):
        """Ensure contact role for an internal configuration can't be deleted by anonymous."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        response = self.client.delete(self.url + f"/{configuration_contact_role.id}")
        self.assertEqual(response.status_code, 401)

    def test_delete_interal_configuration_contact_role_logged_in(self):
        """Ensure contact role for internal configuration can be deleted while no group_id."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        access_headers = create_token()
        response = self.client.delete(
            self.url + f"/{configuration_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_configuration_contact_role_member_in_group(self):
        """Ensure that a contact role for internal configuration can be deleted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="2"
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_configuration_contact_role_admin_in_group(self):
        """Ensure contact role for internal configuration can be deleted by admins of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="1"
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_configuration_contact_role_not_in_group(self):
        """Ensure non members/admins can't delete contact role for internal configuration."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="4"
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_internal_configuration_contact_role_superuser(self):
        """Ensure contact role for internal configuration can still be deleted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="4"
        )
        contact = configuration_contact_role.contact
        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )
        db.session.add_all([other_contact, admin_user])
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{configuration_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_patch_public_configuration_contact_role_anonymous(self):
        """Ensure that a public contact role can't be patched from anonymous."""
        configuration_contact_role = generate_configuration_contact_role()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{configuration_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_patch_public_configuration_contact_role_logged_in(self):
        """Ensure that contact role for public configuration can be patched when no group_id."""
        configuration_contact_role = generate_configuration_contact_role()
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{configuration_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_public_configuration_contact_role_member_in_group(self):
        """Ensure that contact role for public configuration can be patched by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="2")
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_for_archived_configuration(self):
        """Ensure we can't patch if the configuration is archived already."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="2")
        configuration_contact_role.configuration.archived = True
        db.session.add(configuration_contact_role.configuration)
        db.session.commit()

        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_patch_public_configuration_contact_role_admin_in_group(self):
        """Ensure that contact role for public configuration can be patched by admin of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="1")
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_public_configuration_contact_role_not_in_group(self):
        """Ensure contact role for public configuration can't be patched by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="4")
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_public_configuration_contact_role_superuser(self):
        """Ensure that contact role for public configuration can still be patched by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(group_id="4")
        contact = configuration_contact_role.contact
        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )
        db.session.add_all([other_contact, admin_user])
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_configuration_contact_role_anonymous(self):
        """Ensure contact role for an internal configuration can't be patched by anonymous."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{configuration_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_patch_interal_configuration_contact_role_logged_in(self):
        """Ensure contact role for internal configuration can be patched while no group_id."""
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        access_headers = create_token()
        response = self.client.patch(
            self.url + f"/{configuration_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_configuration_contact_role_member_in_group(self):
        """Ensure that a contact role for internal configuration can be patched by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="2"
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_configuration_contact_role_admin_in_group(self):
        """Ensure contact role for internal configuration can be patched by admins of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="1"
        )
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_configuration_contact_role_not_in_group(self):
        """Ensure non members/admins can't patch contact role for internal configuration."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="4"
        )
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_internal_configuration_contact_role_superuser(self):
        """Ensure contact role for internal configuration can still be patched by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration_contact_role = generate_configuration_contact_role(
            internal=True, public=False, group_id="4"
        )
        contact = configuration_contact_role.contact
        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )
        db.session.add_all([other_contact, admin_user])
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(configuration_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{configuration_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_post_public_configuration_contact_role_anonymous(self):
        """Ensure that a public contact role can't be posted from anonymous."""
        configuration = generate_configuration()
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }

        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_post_public_configuration_contact_role_logged_in(self):
        """Ensure that contact role for public configuration can be posted when no group_id."""
        configuration = generate_configuration()
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_public_configuration_contact_role_member_in_group(self):
        """Ensure that contact role for public configuration can be posted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration = generate_configuration(group_id="2")
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_for_archived_configuration(self):
        """Ensure we can't add contacts for archived configurations."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration = generate_configuration(group_id="2")
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_post_public_configuration_contact_role_admin_in_group(self):
        """Ensure that contact role for public configuration can be posted by admin of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        configuration = generate_configuration(group_id="1")
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_public_configuration_contact_role_not_in_group(self):
        """Ensure contact role for public configuration can't be posted by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration = generate_configuration(group_id="4")
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 403)

    def test_post_public_configuration_contact_role_superuser(self):
        """Ensure that contact role for public configuration can still be posted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration = generate_configuration(group_id="4")
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )
        db.session.add_all([other_contact, admin_user])
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_internal_configuration_contact_role_anonymous(self):
        """Ensure contact role for an internal configuration can't be posted by anonymous."""
        configuration = generate_configuration(internal=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_post_interal_configuration_contact_role_logged_in(self):
        """Ensure contact role for internal configuration can be posted while no group_id."""
        configuration = generate_configuration(internal=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_internal_configuration_contact_role_member_in_group(self):
        """Ensure that a contact role for internal configuration can be posted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        configuration = generate_configuration(
            internal=True, public=False, group_id="2"
        )
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_internal_configuration_contact_role_admin_in_group(self):
        """Ensure contact role for internal configuration can be posted by admins of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        configuration = generate_configuration(
            internal=True, public=False, group_id="1"
        )
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_internal_configuration_contact_role_not_in_group(self):
        """Ensure contact role for internal configuration can't be posted by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration = generate_configuration(
            internal=True, public=False, group_id="4"
        )
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 403)

    def test_post_internal_configuration_contact_role_superuser(self):
        """Ensure contact role for internal configuration can still be posted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        configuration = generate_configuration(
            internal=True, public=False, group_id="4"
        )
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(configuration.id),
                            "type": "configuration",
                        },
                    },
                    "contact": {
                        "data": {
                            "id": str(contact.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )
        db.session.add_all([other_contact, admin_user])
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")
