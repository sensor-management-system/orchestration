# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the site contact roles."""

from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Site, SiteContactRole, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestSiteContacts(BaseTestCase):
    """Test class for the site contacts."""

    url = base_url + "/site-contact-roles"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@somewhere"
        )
        self.super_contact = Contact(
            given_name="super", family_name="contact", email="super.contact@somewhere"
        )
        self.normal_user = User(
            contact=self.normal_contact,
            subject=self.normal_contact.email,
        )
        self.super_user = User(
            contact=self.super_contact,
            subject=self.super_contact.email,
            is_superuser=True,
        )
        self.internal_site = Site(
            label="internal",
            is_internal=True,
            is_public=False,
            created_by=self.normal_user,
            updated_by=self.normal_user,
        )
        self.public_site = Site(
            label="public",
            is_internal=False,
            is_public=True,
            created_by=self.normal_user,
            updated_by=self.normal_user,
        )

        db.session.add_all(
            [
                self.internal_site,
                self.public_site,
                self.normal_contact,
                self.normal_user,
                self.super_contact,
                self.super_user,
            ]
        )
        db.session.commit()

    def test_query_all_public(self):
        """Ensure we get some entries for the list query for public sites."""
        contact_role1 = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        contact_role2 = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="Administrator",
        )
        db.session.add_all([contact_role1, contact_role2])

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 2)
        self.assertEqual(resp.json["data"][0]["attributes"]["role_name"], "PI")
        self.assertEqual(
            resp.json["data"][1]["attributes"]["role_name"], "Administrator"
        )

    def test_query_with_internal_anonymous(self):
        """Ensure we get don't show contacts for internal sites without login."""
        contact_role1 = SiteContactRole(
            contact=self.normal_contact,
            site=self.internal_site,
            role_name="PI",
        )
        contact_role2 = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="Administrator",
        )
        db.session.add_all([contact_role1, contact_role2])

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 1)
        self.assertEqual(
            resp.json["data"][0]["attributes"]["role_name"], "Administrator"
        )

    def test_query_with_internal_normal_user(self):
        """Ensure we get show contacts for internal sites with login."""
        contact_role1 = SiteContactRole(
            contact=self.normal_contact,
            site=self.internal_site,
            role_name="PI",
        )
        contact_role2 = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="Administrator",
        )
        db.session.add_all([contact_role1, contact_role2])

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 2)
        self.assertEqual(resp.json["data"][0]["attributes"]["role_name"], "PI")
        self.assertEqual(
            resp.json["data"][1]["attributes"]["role_name"], "Administrator"
        )

    def test_query_with_internal_normal_user_for_specific_sites(self):
        """Ensure we get show contacts for internal sites with login."""
        contact_role1 = SiteContactRole(
            contact=self.normal_contact,
            site=self.internal_site,
            role_name="PI",
        )
        contact_role2 = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="Administrator",
        )
        db.session.add_all([contact_role1, contact_role2])

        with self.run_requests_as(self.normal_user):
            resp_public = self.client.get(
                f"{base_url}/sites/{self.public_site.id}/site-contact-roles"
            )
            resp_internal = self.client.get(
                f"{base_url}/sites/{self.internal_site.id}/site-contact-roles"
            )
        self.assertEqual(resp_public.status_code, 200)
        self.assertEqual(resp_internal.status_code, 200)
        self.assertEqual(len(resp_public.json["data"]), 1)
        self.assertEqual(len(resp_internal.json["data"]), 1)
        self.assertEqual(
            resp_public.json["data"][0]["attributes"]["role_name"], "Administrator"
        )
        self.assertEqual(resp_internal.json["data"][0]["attributes"]["role_name"], "PI")

    def test_post_anonymous(self):
        """Ensure that we can't post site contact roles without login."""
        payload = {
            "data": {
                "type": "site_contact_role",
                "attributes": {
                    "role_uri": "",
                    "role_name": "PI",
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": str(self.public_site.id),
                            "type": "site",
                        }
                    },
                    "contact": {
                        "data": {"id": str(self.normal_contact.id), "type": "contact"}
                    },
                },
            }
        }

        resp = self.client.post(
            self.url, json=payload, headers={"Content-Type": "application/vnd.api+json"}
        )
        self.assertEqual(resp.status_code, 401)

    def test_post_no_group_member(self):
        """Ensure that we can't post for site groups that we are no member in."""
        self.public_site.group_ids = ["123"]
        payload = {
            "data": {
                "type": "site_contact_role",
                "attributes": {
                    "role_uri": "",
                    "role_name": "PI",
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": str(self.public_site.id),
                            "type": "site",
                        }
                    },
                    "contact": {
                        "data": {"id": str(self.normal_contact.id), "type": "contact"}
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=[],
                    administrated_permission_groups=[],
                )
                resp = self.client.post(
                    self.url,
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 403)

    def test_post_group_member(self):
        """Ensure that we can post for site groups that we are member in."""
        self.public_site.group_ids = ["123"]
        payload = {
            "data": {
                "type": "site_contact_role",
                "attributes": {
                    "role_uri": "",
                    "role_name": "PI",
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": str(self.public_site.id),
                            "type": "site",
                        }
                    },
                    "contact": {
                        "data": {"id": str(self.normal_contact.id), "type": "contact"}
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=["123"],
                    administrated_permission_groups=[],
                )
                resp = self.client.post(
                    self.url,
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 201)

    def test_post_group_administrator(self):
        """Ensure that we can post for site groups that we are admin in."""
        self.public_site.group_ids = ["123"]
        payload = {
            "data": {
                "type": "site_contact_role",
                "attributes": {
                    "role_uri": "",
                    "role_name": "PI",
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": str(self.public_site.id),
                            "type": "site",
                        }
                    },
                    "contact": {
                        "data": {"id": str(self.normal_contact.id), "type": "contact"}
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=[],
                    administrated_permission_groups=["123"],
                )
                resp = self.client.post(
                    self.url,
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 201)

    def test_post_super_user(self):
        """Ensure that super users can post for site groups."""
        payload = {
            "data": {
                "type": "site_contact_role",
                "attributes": {
                    "role_uri": "",
                    "role_name": "PI",
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": str(self.public_site.id),
                            "type": "site",
                        }
                    },
                    "contact": {
                        "data": {"id": str(self.normal_contact.id), "type": "contact"}
                    },
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)

    def test_after_post_site_update_description(self):
        """Ensure that update the update description of the site when posting."""
        payload = {
            "data": {
                "type": "site_contact_role",
                "attributes": {
                    "role_uri": "",
                    "role_name": "PI",
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": str(self.public_site.id),
                            "type": "site",
                        }
                    },
                    "contact": {
                        "data": {"id": str(self.normal_contact.id), "type": "contact"}
                    },
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        site = db.session.query(Site).filter_by(id=self.public_site.id).first()
        self.assertEqual(site.update_description, "create;contact")
        # And we also update the updated_by by adding the contact.
        self.assertEqual(site.updated_by, self.super_user)

    def test_get_one_non_existing(self):
        """Ensure we get a 404 if we ask for a non existing contact role."""
        resp = self.client.get(self.url + "/999999999999")
        self.assertEqual(resp.status_code, 404)

    def test_get_one_internal_anonymous(self):
        """Ensure that we don't allow to get contact roles for internal sites without login."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.internal_site,
            role_name="PI",
        )
        db.session.add(contact_role)
        db.session.commit()

        resp = self.client.get(f"{self.url}/{contact_role.id}")
        # Both 401 or 403 are fine.
        self.assertIn(resp.status_code, [401, 403])

    def test_get_one_public_anonymous(self):
        """Ensure that we allow to get contact roles for public sites without login."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(contact_role)
        db.session.commit()

        resp = self.client.get(f"{self.url}/{contact_role.id}")
        self.assertEqual(resp.status_code, 200)

    def test_get_one_internal_normal_user(self):
        """Ensure that we allow to get contact roles for internal sites with login."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.internal_site,
            role_name="PI",
        )
        db.session.add(contact_role)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(f"{self.url}/{contact_role.id}")
            self.assertEqual(resp.status_code, 200)

    def test_patch_anonymous(self):
        """Ensure we don't allow patching contact roles without login."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(contact_role)
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": str(contact_role.id),
                "attributes": {
                    "role_name": "Administrator",
                },
            },
        }

        resp = self.client.patch(
            f"{self.url}/{contact_role.id}",
            json=payload,
            headers={"Content-Type": "application/vnd.api+json"},
        )
        self.assertEqual(resp.status_code, 401)

    def test_patch_no_member(self):
        """Ensure we don't allow patching contact roles without membership in group of site."""
        self.public_site.group_ids = ["123"]
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([self.public_site, contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": str(contact_role.id),
                "attributes": {
                    "role_name": "Administrator",
                },
            },
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=[],
                    administrated_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.url}/{contact_role.id}",
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 403)

    def test_patch_group_member(self):
        """Ensure we allow patching contact roles for members in group of site."""
        self.public_site.group_ids = ["123"]
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([self.public_site, contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": str(contact_role.id),
                "attributes": {
                    "role_name": "Administrator",
                },
            },
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=["123"],
                    administrated_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.url}/{contact_role.id}",
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 200)

    def test_patch_group_admin(self):
        """Ensure we allow patching contact roles for admins in group of site."""
        self.public_site.group_ids = ["123"]
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([self.public_site, contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": str(contact_role.id),
                "attributes": {
                    "role_name": "Administrator",
                },
            },
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=[],
                    administrated_permission_groups=["123"],
                )
                resp = self.client.patch(
                    f"{self.url}/{contact_role.id}",
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 200)

    def test_patch_super_user(self):
        """Ensure we allow patching contact roles for super users."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(self.public_site)
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": str(contact_role.id),
                "attributes": {
                    "role_name": "Administrator",
                },
            },
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.patch(
                f"{self.url}/{contact_role.id}",
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 200)

    def test_patch_archived_site(self):
        """Ensure we don't allow patching for archived sites."""
        self.public_site.archived = True
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([self.public_site, contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": str(contact_role.id),
                "attributes": {
                    "role_name": "Administrator",
                },
            },
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.patch(
                f"{self.url}/{contact_role.id}",
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 403)

    def test_after_patch_updated_site_update_description(self):
        """Ensure we update the update description after patching the contact role."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(self.public_site)
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "id": str(contact_role.id),
                "attributes": {
                    "role_name": "Administrator",
                },
            },
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.patch(
                f"{self.url}/{contact_role.id}",
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 200)
        site = db.session.query(Site).filter_by(id=self.public_site.id).first()
        self.assertEqual(site.update_description, "update;contact")
        self.assertEqual(site.updated_by, self.super_user)

    def test_delete_anonymous(self):
        """Ensure we don't allow deleting contact roles without login."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(contact_role)
        db.session.commit()

        resp = self.client.delete(
            f"{self.url}/{contact_role.id}",
        )
        self.assertEqual(resp.status_code, 401)

    def test_delete_no_member(self):
        """Ensure we don't allow deleting contact roles without membership in group of site."""
        self.public_site.group_ids = ["123"]
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([self.public_site, contact_role])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=[],
                    administrated_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{contact_role.id}",
                )
        self.assertEqual(resp.status_code, 403)

    def test_delete_group_member(self):
        """Ensure we don't allow deleting contact roles for members in group of site."""
        self.public_site.group_ids = ["123"]
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([self.public_site, contact_role])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=["123"],
                    administrated_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{contact_role.id}",
                )
        self.assertEqual(resp.status_code, 200)

    def test_delete_group_admin(self):
        """Ensure we don't allow deleting contact roles for admins in group of site."""
        self.public_site.group_ids = ["123"]
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([self.public_site, contact_role])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id="1234",
                    username="abc",
                    membered_permission_groups=[],
                    administrated_permission_groups=["123"],
                )
                resp = self.client.delete(
                    f"{self.url}/{contact_role.id}",
                )
        self.assertEqual(resp.status_code, 200)

    def test_delete_super_user(self):
        """Ensure we allow deleting contact roles for super users."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(self.public_site)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            resp = self.client.delete(
                f"{self.url}/{contact_role.id}",
            )
        self.assertEqual(resp.status_code, 200)

    def test_after_delete_update_description(self):
        """Ensure we update the update description of the site after deleting the contact."""
        contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(self.public_site)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            resp = self.client.delete(
                f"{self.url}/{contact_role.id}",
            )
        self.assertEqual(resp.status_code, 200)

        site = db.session.query(Site).filter_by(id=self.public_site.id).first()
        self.assertEqual(site.update_description, "delete;contact")
        self.assertEqual(site.updated_by, self.super_user)

    def test_delete_related_contact(self):
        """Ensure we don't have orphans if we delete the contact."""
        # We can't delete the normal contact here, as it is still needed
        # for user relation.
        dummy_contact = Contact(
            given_name="Dummy J.",
            family_name="Contact",
            email="dj@dummy.contacts.localhost",
        )
        site_contact_role = SiteContactRole(
            contact=dummy_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add_all([site_contact_role, dummy_contact])
        db.session.commit()
        site_contact_role_id = site_contact_role.id
        self.assertIsNotNone(site_contact_role_id)
        db.session.delete(site_contact_role.contact)
        db.session.commit()

        # It should remove the contact role as well.
        reloaded = (
            db.session.query(SiteContactRole).filter_by(id=site_contact_role_id).first()
        )
        self.assertIsNone(reloaded)

    def test_delete_related_site(self):
        """Ensure we don't have orphans if we delete the site."""
        site_contact_role = SiteContactRole(
            contact=self.normal_contact,
            site=self.public_site,
            role_name="PI",
        )
        db.session.add(site_contact_role)
        db.session.commit()
        site_contact_role_id = site_contact_role.id
        self.assertIsNotNone(site_contact_role_id)
        db.session.delete(site_contact_role.site)
        db.session.commit()

        # It should remove the contact role as well.
        reloaded = (
            db.session.query(SiteContactRole).filter_by(id=site_contact_role_id).first()
        )
        self.assertIsNone(reloaded)

    def test_ensure_unique_constraint_on_post(self):
        """Ensure that we have a unique constraint for role, site and contact."""
        contact = Contact(
            given_name="A", family_name="Contact", email="a.contact@localhost"
        )
        super_user = User(contact=contact, subject=contact.email, is_superuser=True)

        site = Site(label="test site", is_internal=True)
        role_name = "Owner"
        role_uri = "https://cv/roles/1"

        contact_role = SiteContactRole(
            contact=contact,
            site=site,
            role_name=role_name,
            role_uri=role_uri,
        )

        db.session.add_all([contact, super_user, site, contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "site_contact_role",
                "attributes": {
                    "role_name": role_name,
                    "role_uri": role_uri,
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": site.id,
                            "type": "site",
                        },
                    },
                    "contact": {"data": {"id": contact.id, "type": "contact"}},
                },
            }
        }

        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                json=payload,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 409)

    def test_ensure_unique_constraint_on_patch(self):
        """Ensure that we have a unique constraint for role, site and contact also for changes."""
        contact = Contact(
            given_name="A", family_name="Contact", email="a.contact@localhost"
        )
        super_user = User(contact=contact, subject=contact.email, is_superuser=True)

        site = Site(label="test site", is_internal=True)
        role_name1 = "Owner"
        role_uri1 = "https://cv/roles/1"

        contact_role1 = SiteContactRole(
            contact=contact,
            site=site,
            role_name=role_name1,
            role_uri=role_uri1,
        )

        role_name2 = "PI"
        role_uri2 = "https://cv/roles/2"

        contact_role2 = SiteContactRole(
            contact=contact,
            site=site,
            role_name=role_name2,
            role_uri=role_uri2,
        )

        db.session.add_all([contact, super_user, site, contact_role1, contact_role2])
        db.session.commit()

        # It is not possible to add this for the very same site, contact & role.
        payload = {
            "data": {
                "type": "site_contact_role",
                "id": contact_role2.id,
                "attributes": {
                    "role_name": role_name1,
                    "role_uri": role_uri1,
                },
                "relationships": {
                    "site": {
                        "data": {
                            "id": site.id,
                            "type": "site",
                        },
                    },
                    "contact": {"data": {"id": contact.id, "type": "contact"}},
                },
            }
        }

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{contact_role2.id}",
                json=payload,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 409)
