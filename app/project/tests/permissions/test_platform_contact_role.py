"""Tests for the platform contact roles with permission management."""

import json
from unittest.mock import patch

from project import base_url, db
from project.api.models import Contact, Platform, PlatformContactRole, User
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, generate_userinfo_data
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def generate_platform(
    public=True,
    private=False,
    internal=False,
    group_ids=None,
):
    """Generate a platform to work with."""
    if not group_ids:
        group_ids = []
    platform = Platform(
        short_name="short_name test",
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    db.session.add(platform)
    db.session.commit()
    return platform


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


def generate_platform_contact_role(
    public=True,
    private=False,
    internal=False,
    group_ids=None,
):
    """Generate a platform contact role to work with."""
    platform = generate_platform(
        public=public, private=private, internal=internal, group_ids=group_ids
    )
    contact = generate_contact()
    platform_contact_role = PlatformContactRole(
        platform=platform,
        contact=contact,
        role_name="Operator",
        role_uri="https://server/cv/api/v1/contactroles/3",
    )
    db.session.add(platform_contact_role)
    db.session.commit()
    return platform_contact_role


class TestPlatformContactRolePermissions(BaseTestCase):
    """Tests for the platform contact roles."""

    url = base_url + "/platform-contact-roles"
    object_type = "platform_contact_role"

    def test_getlist_public_platform_contact_role(self):
        """Ensure that a contact role for a public platform will be listed."""
        platform_contact_role = generate_platform_contact_role()
        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )
        self.assertEqual(role.role_name, platform_contact_role.role_name)
        self.assertEqual(role.role_uri, platform_contact_role.role_uri)
        self.assertEqual(role.platform, platform_contact_role.platform)
        self.assertEqual(
            role.platform.is_public, platform_contact_role.platform.is_public
        )
        self.assertEqual(role.platform.is_public, True)
        self.assertEqual(role.contact, platform_contact_role.contact)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"][0]["id"], str(role.id))

    def test_getlist_internal_platform_contact_role_anonymous(self):
        """Ensure that a contact role for an internal platform is not listed for anonymous."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )

        self.assertEqual(
            role.platform.is_internal, platform_contact_role.platform.is_internal
        )
        self.assertEqual(role.platform.is_internal, True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_getlist_interal_platform_contact_role_logged_in(self):
        """Ensure that a contact role for an internal platform is listed for logged in users."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )

        self.assertEqual(
            role.platform.is_internal, platform_contact_role.platform.is_internal
        )
        self.assertEqual(role.platform.is_internal, True)

        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"][0]["id"], str(role.id))

    def test_getlist_private_platform_contact_role_anonymous(self):
        """Ensure get collection for anonymous users & private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )

        self.assertEqual(
            role.platform.is_private, platform_contact_role.platform.is_private
        )
        self.assertEqual(role.platform.is_private, True)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_getlist_private_platform_contact_role_owner(self):
        """Ensure get collection for owner of private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )

        self.assertEqual(
            role.platform.is_private, platform_contact_role.platform.is_private
        )
        self.assertEqual(role.platform.is_private, True)

        access_headers = create_token({"sub": user.subject})
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"][0]["id"], str(role.id))

    def test_getlist_private_platform_contact_role_different_user(self):
        """Ensure get collection for different user on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )

        self.assertEqual(
            role.platform.is_private, platform_contact_role.platform.is_private
        )
        self.assertEqual(role.platform.is_private, True)

        access_headers = create_token(
            {
                "sub": "x" + user.subject,
                "given_name": "x" + contact.given_name,
                "family_name": "x" + contact.family_name,
                "email": "x" + contact.email,
            }
        )
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_getlist_private_platform_contact_role_different_admin(self):
        """Ensure get collection for different user (admin) on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )
        db.session.add_all(
            [
                user,
                platform_contact_role,
                other_contact,
                admin_user,
                platform_contact_role.platform,
            ]
        )
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(response.json["data"][0]["id"], str(platform_contact_role.id))

    def test_getone_public_platform_contact_role(self):
        """Ensure that a public contact role can be listed."""
        platform_contact_role = generate_platform_contact_role()
        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )
        response = self.client.get(self.url + f"/{role.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(role.id))

    def test_getone_internal_platform_contact_role_anonymous(self):
        """Ensure taht a contact role for an internal platform is not accessble for anonymous."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )
        response = self.client.get(self.url + f"/{role.id}")
        self.assertEqual(response.status_code, 401)

    def test_getone_interal_platform_contact_role_logged_in(self):
        """Ensure that a contact role for an internal platform is listed for logged in users."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role.id)
            .one()
        )
        access_headers = create_token()
        response = self.client.get(self.url + f"/{role.id}", headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(role.id))

    def test_getone_private_platform_contact_role_anonymous(self):
        """Ensure get details for anonymous users & private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        response = self.client.get(self.url + f"/{platform_contact_role.id}")
        self.assertEqual(response.status_code, 401)

    def test_getone_private_platform_contact_role_owner(self):
        """Ensure that the owner of a private platform can access the contact role."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        access_headers = create_token({"sub": user.subject})
        response = self.client.get(
            f"{self.url}/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(platform_contact_role.id))

    def test_getone_private_platform_contact_role_different_user(self):
        """Ensure get one for different user on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        access_headers = create_token(
            {
                "sub": "x" + user.subject,
                "given_name": "x" + contact.given_name,
                "family_name": "x" + contact.family_name,
                "email": "x" + contact.email,
            }
        )

        response = self.client.get(
            self.url + f"/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_getone_private_platform_contact_role_different_admin(self):
        """Ensure get one for different user (but admin) on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user

        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )

        db.session.add_all(
            [
                user,
                platform_contact_role,
                other_contact,
                admin_user,
                platform_contact_role.platform,
            ]
        )
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )

        response = self.client.get(
            self.url + f"/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(platform_contact_role.id))

    def test_delete_public_platform_contact_role_anonymous(self):
        """Ensure that a public contact role can't be deleted from anymous."""
        platform_contact_role = generate_platform_contact_role()
        response = self.client.delete(self.url + f"/{platform_contact_role.id}")
        self.assertEqual(response.status_code, 401)

    def test_delete_public_platform_contact_role_logged_in(self):
        """Ensure that contact role for public platform can be deleted when no group_ids."""
        platform_contact_role = generate_platform_contact_role()
        access_headers = create_token()
        response = self.client.delete(
            self.url + f"/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_public_platform_contact_role_member_in_group(self):
        """Ensure that contact role for public platform can be deleted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["2"])
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_public_platform_contact_role_member_for_archived_platform(self):
        """Ensure that contact role for an archived platform can't be deleted."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["2"])
        platform_contact_role.platform.archived = True
        db.session.add(platform_contact_role.platform)
        db.session.commit()
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 409)

    def test_delete_public_platform_contact_role_admin_in_group(self):
        """Ensure that contact role for public platform can be deleted by admin of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["1"])
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_public_platform_contact_role_not_in_group(self):
        """Ensure that contact role for public platform can't be deleted by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["4"])
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_public_platform_contact_role_superuser(self):
        """Ensure that contact role for public platform can still be deleted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["4"])
        contact = platform_contact_role.contact
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
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_platform_contact_role_anonymous(self):
        """Ensure taht a contact role for an internal platform can't be deleted by anonymous."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        response = self.client.delete(self.url + f"/{platform_contact_role.id}")
        self.assertEqual(response.status_code, 401)

    def test_delete_interal_platform_contact_role_logged_in(self):
        """Ensure that a contact role for internal platform can be deleted while no group_ids."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        access_headers = create_token()
        response = self.client.delete(
            self.url + f"/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_platform_contact_role_member_in_group(self):
        """Ensure that a contact role for internal platform can be deleted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["2"]
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_platform_contact_role_admin_in_group(self):
        """Ensure that a contact role for internal platform can be deleted by admins of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["1"]
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_internal_platform_contact_role_not_in_group(self):
        """Ensure contact role for internal platform can't be deleted by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["4"]
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.delete(
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_internal_platform_contact_role_superuser(self):
        """Ensure that contact role for internal platform can still be deleted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["4"]
        )
        contact = platform_contact_role.contact
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
                self.url + f"/{platform_contact_role.id}", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_private_platform_contact_role_anonymous(self):
        """Ensure delete for anonymous user & private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        response = self.client.delete(self.url + f"/{platform_contact_role.id}")
        self.assertEqual(response.status_code, 401)

    def test_delete_private_platform_contact_role_owner(self):
        """Ensure that the owner of a private platform can delete the contact role."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        access_headers = create_token({"sub": user.subject})
        response = self.client.delete(
            f"{self.url}/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_private_platform_contact_role_different_user(self):
        """Ensure delete for different user on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        access_headers = create_token(
            {
                "sub": "x" + user.subject,
                "given_name": "x" + contact.given_name,
                "family_name": "x" + contact.family_name,
                "email": "x" + contact.email,
            }
        )

        response = self.client.delete(
            self.url + f"/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_private_platform_contact_role_different_admin(self):
        """Ensure delete for different user (but admin) on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user

        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )

        db.session.add_all(
            [
                user,
                platform_contact_role,
                other_contact,
                admin_user,
                platform_contact_role.platform,
            ]
        )
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )

        response = self.client.delete(
            self.url + f"/{platform_contact_role.id}", headers=access_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_public_platform_contact_role_anonymous(self):
        """Ensure that a public contact role can't be patched from anonymous."""
        platform_contact_role = generate_platform_contact_role()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_patch_public_platform_contact_role_logged_in(self):
        """Ensure that contact role for public platform can be patched when no group_ids."""
        platform_contact_role = generate_platform_contact_role()
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_public_platform_contact_role_member_in_group(self):
        """Ensure that contact role for public platform can be patched by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["2"])
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_public_platform_contact_role_member_for_archived_platform(self):
        """Ensure that contact role for archived platform can't be patched.."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["2"])
        platform_contact_role.platform.archived = True
        db.session.add(platform_contact_role.platform)
        db.session.commit()

        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_patch_public_platform_contact_role_admin_in_group(self):
        """Ensure that contact role for public platform can be patched by admin of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["1"])
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_public_platform_contact_role_not_in_group(self):
        """Ensure that contact role for public platform can't be patched by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["4"])
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_public_platform_contact_role_superuser(self):
        """Ensure that contact role for public platform can still be patched by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(group_ids=["4"])
        contact = platform_contact_role.contact
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
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_platform_contact_role_anonymous(self):
        """Ensure that a contact role for an internal platform can't be patched by anonymous."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_patch_interal_platform_contact_role_logged_in(self):
        """Ensure that a contact role for internal platform can be patched while no group_ids."""
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        access_headers = create_token()
        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_platform_contact_role_member_in_group(self):
        """Ensure that a contact role for internal platform can be patched by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["2"]
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_platform_contact_role_admin_in_group(self):
        """Ensure that a contact role for internal platform can be patched by admins of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["1"]
        )
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_internal_platform_contact_role_not_in_group(self):
        """Ensure contact role for internal platform can't be patched by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["4"]
        )
        access_headers = create_token()
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_internal_platform_contact_role_superuser(self):
        """Ensure that contact role for internal platform can still be patched by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform_contact_role = generate_platform_contact_role(
            internal=True, public=False, group_ids=["4"]
        )
        contact = platform_contact_role.contact
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
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            response = self.client.patch(
                self.url + f"/{platform_contact_role.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_private_platform_contact_role_anonymous(self):
        """Ensure patch for anonymous user & private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_patch_private_platform_contact_role_owner(self):
        """Ensure that the owner of a private platform can patch the contact role."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        access_headers = create_token({"sub": user.subject})
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }
        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_patch_private_platform_contact_role_different_user(self):
        """Ensure patch for different user on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user
        db.session.add_all(
            [user, platform_contact_role, platform_contact_role.platform]
        )
        db.session.commit()

        access_headers = create_token(
            {
                "sub": "x" + user.subject,
                "given_name": "x" + contact.given_name,
                "family_name": "x" + contact.family_name,
                "email": "x" + contact.email,
            }
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }

        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 403)

    def test_patch_private_platform_contact_role_different_admin(self):
        """Ensure patch for different user (but admin) on private platform."""
        platform_contact_role = generate_platform_contact_role(
            private=True, public=False
        )
        contact = platform_contact_role.contact
        user = User(contact=contact, subject=contact.email)
        platform_contact_role.platform.created_by = user

        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )

        db.session.add_all(
            [
                user,
                platform_contact_role,
                other_contact,
                admin_user,
                platform_contact_role.platform,
            ]
        )
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        payload = {
            "data": {
                "type": self.object_type,
                "id": str(platform_contact_role.id),
                "attributes": {"role_name": "new role"},
            }
        }

        response = self.client.patch(
            self.url + f"/{platform_contact_role.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "new role")

    def test_post_public_platform_contact_role_anonymous(self):
        """Ensure that a public contact role can't be posted from anonymous."""
        platform = generate_platform()
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_public_platform_contact_role_logged_in(self):
        """Ensure that contact role for public platform can be posted when no group_ids."""
        platform = generate_platform()
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_public_platform_contact_role_member_in_group(self):
        """Ensure that contact role for public platform can be posted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform = generate_platform(group_ids=["2"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_archived_platform(self):
        """Ensure we can't post for archived platforms."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform = generate_platform(group_ids=["2"])
        platform.archived = True
        db.session.add(platform)
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
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_public_platform_contact_role_admin_in_group(self):
        """Ensure that contact role for public platform can be posted by admin of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        platform = generate_platform(group_ids=["1"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_public_platform_contact_role_not_in_group(self):
        """Ensure that contact role for public platform can't be posted by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform = generate_platform(group_ids=["4"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_public_platform_contact_role_superuser(self):
        """Ensure that contact role for public platform can still be posted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform = generate_platform(group_ids=["4"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_internal_platform_contact_role_anonymous(self):
        """Ensure that a contact role for an internal platform can't be posted by anonymous."""
        platform = generate_platform(internal=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_interal_platform_contact_role_logged_in(self):
        """Ensure that a contact role for internal platform can be posted while no group_ids."""
        platform = generate_platform(internal=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_internal_platform_contact_role_member_in_group(self):
        """Ensure that a contact role for internal platform can be posted by members."""
        self.assertIn("2", IDL_USER_ACCOUNT.membered_permission_groups)
        platform = generate_platform(internal=True, public=False, group_ids=["2"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_internal_platform_contact_role_admin_in_group(self):
        """Ensure that a contact role for internal platform can be posted by admins of group."""
        self.assertIn("1", IDL_USER_ACCOUNT.administrated_permission_groups)
        platform = generate_platform(internal=True, public=False, group_ids=["1"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_internal_platform_contact_role_not_in_group(self):
        """Ensure contact role for internal platform can't be posted by non members/admins."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform = generate_platform(internal=True, public=False, group_ids=["4"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_internal_platform_contact_role_superuser(self):
        """Ensure that contact role for internal platform can still be posted by superusers."""
        self.assertFalse("4" in IDL_USER_ACCOUNT.administrated_permission_groups)
        self.assertFalse("4" in IDL_USER_ACCOUNT.membered_permission_groups)
        platform = generate_platform(internal=True, public=False, group_ids=["4"])
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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

    def test_post_private_platform_contact_role_anonymous(self):
        """Ensure post for anonymous user & private platform."""
        platform = generate_platform(private=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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
        user = User(contact=contact, subject=contact.email)
        platform.created_by = user
        db.session.add_all([user, platform])
        db.session.commit()

        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(response.status_code, 401)

    def test_post_private_platform_contact_role_owner(self):
        """Ensure that the owner of a private platform can post the contact role."""
        platform = generate_platform(private=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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
        user = User(contact=contact, subject=contact.email)
        platform.created_by = user
        db.session.add_all([user, platform])
        db.session.commit()

        access_headers = create_token({"sub": user.subject})
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")

    def test_post_private_platform_contact_role_different_user(self):
        """Ensure post for different user on private platform."""
        platform = generate_platform(private=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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
        user = User(contact=contact, subject=contact.email)
        platform.created_by = user
        db.session.add_all([user, platform])
        db.session.commit()

        access_headers = create_token(
            {
                "sub": "x" + user.subject,
                "given_name": "x" + contact.given_name,
                "family_name": "x" + contact.family_name,
                "email": "x" + contact.email,
            }
        )

        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 403)

    def test_post_private_platform_contact_role_different_admin(self):
        """Ensure post for different user (but admin) on private platform."""
        platform = generate_platform(private=True, public=False)
        contact = generate_contact()
        payload = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "role_name": "dummy name",
                    "role_uri": "dummy uri",
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
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
        user = User(contact=contact, subject=contact.email)
        platform.created_by = user

        other_contact = Contact(
            email="x" + contact.email,
            given_name="x" + contact.given_name,
            family_name="x" + contact.family_name,
        )
        admin_user = User(
            contact=other_contact, subject=other_contact.email, is_superuser=True
        )

        db.session.add_all([user, platform, other_contact, admin_user])
        db.session.commit()
        access_headers = create_token(
            {
                "sub": admin_user.subject,
            }
        )
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
            headers=access_headers,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["data"]["attributes"]["role_name"], "dummy name")
