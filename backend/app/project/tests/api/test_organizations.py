# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the organizations endpoints."""

import json

from project import base_url
from project.api.models import Contact, Organization, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, Fixtures

fixtures = Fixtures()


@fixtures.register("organization1", scope=lambda: db.session)
def create_organiaztion1():
    """Create a first organization for the tests."""
    result = Organization(name="organization1")
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("organization2", scope=lambda: db.session)
def create_organiaztion2():
    """Create a second organization for the tests."""
    result = Organization(name="organization2")
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("contact1", scope=lambda: db.session)
def create_contact1():
    """Create a single contact so that it can be used within the tests."""
    result = Contact(
        given_name="first", family_name="contact", email="first.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user", scope=lambda: db.session)
@fixtures.use(["super_user_contact"])
def create_super_user(super_user_contact):
    """Create super user to use it in the tests."""
    result = User(
        contact=super_user_contact, subject=super_user_contact.email, is_superuser=True
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user_contact", scope=lambda: db.session)
def create_super_user_contact():
    """Create a contact that can be used to make a super user."""
    result = Contact(
        given_name="super", family_name="contact", email="super.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestOrganizations(BaseTestCase):
    """Test class for the organizations api."""

    url = base_url + "/organizations"

    def test_get_list_emty(self):
        """Ensure we can query the empty list."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    @fixtures.use
    def test_get_list(self, organization1, organization2):
        """Ensure we can query the list with some content."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json["data"]), 2)
        self.assertEqual(resp.json["data"][0]["attributes"]["name"], organization1.name)
        self.assertEqual(resp.json["data"][1]["attributes"]["name"], organization2.name)

    def test_get_one_non_existing(self):
        """Ensure we get 404 on get detail for non existing organizations."""
        resp = self.client.get(self.url + "/12345678901234")
        self.assertEqual(resp.status_code, 404)

    @fixtures.use
    def test_get_one(self, organization1):
        """Ensure we get the attributes for an existing organization."""
        resp = self.client.get(f"{self.url}/{organization1.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"]["attributes"]["name"], organization1.name)

    def test_post_anonymous(self):
        """Ensure we can't create organizations without a user."""
        payload = {
            "data": {
                "type": "organization",
                "attributes": {
                    "name": "New organization",
                },
            }
        }
        resp = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/vnd.api+json"
        )
        self.assertEqual(resp.status_code, 401)

    @fixtures.use
    def test_post_user(self, user1):
        """Ensure we can't create organization as a normal user."""
        payload = {
            "data": {
                "type": "organization",
                "attributes": {
                    "name": "New organization",
                },
            }
        }
        with self.run_requests_as(user1):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 403)

    @fixtures.use
    def test_post_super_user(self, super_user):
        """Ensure we can create organizations as a super user."""
        payload = {
            "data": {
                "type": "organization",
                "attributes": {
                    "name": "New organization",
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(
            resp.json["data"]["attributes"]["name"],
            payload["data"]["attributes"]["name"],
        )

    @fixtures.use
    def test_patch_as_super_user(self, organization1, super_user):
        """Ensure that a super user can update the organization data."""
        payload = {
            "data": {
                "type": "organization",
                "id": str(organization1.id),
                "attributes": {
                    "name": "fancy new organization",
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{organization1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json["data"]["attributes"]["name"],
            payload["data"]["attributes"]["name"],
        )

    @fixtures.use
    def test_patch_non_existing_as_super_user(self, super_user):
        """Ensure we get 404 if the organization doesn't exist."""
        payload = {
            "data": {
                "type": "organization",
                "id": "12345678901234",
                "attributes": {
                    "name": "fancy new organization",
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/12345678901234",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 404)

    @fixtures.use
    def test_patch_as_normal_user(self, organization1, user1):
        """Ensure a normal user can't change the organization data."""
        payload = {
            "data": {
                "type": "organization",
                "id": str(organization1.id),
                "attributes": {
                    "name": "fancy new organization",
                },
            }
        }
        with self.run_requests_as(user1):
            resp = self.client.patch(
                f"{self.url}/{organization1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 403)

    @fixtures.use
    def test_patch_anonymous(self, organization1):
        """Ensure an anonymous user can't patch the organization."""
        payload = {
            "data": {
                "type": "organization",
                "id": str(organization1.id),
                "attributes": {
                    "name": "fancy new organization",
                },
            }
        }
        resp = self.client.patch(
            f"{self.url}/{organization1.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.assertEqual(resp.status_code, 401)

    @fixtures.use
    def test_delete_as_super_user(self, organization1, super_user):
        """Ensure a super user can delete an organization."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(f"{self.url}/{organization1.id}")
        self.assertEqual(resp.status_code, 200)

        self.assertIsNone(
            db.session.query(Organization).filter_by(id=organization1.id).first()
        )

    @fixtures.use
    def test_delete_non_existing_as_super_user(self, super_user):
        """Ensure we get 404 on delete if the organization doesn't exist."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(f"{self.url}/12345678901234")
        self.assertEqual(resp.status_code, 404)

    @fixtures.use
    def test_delete_as_normal_user(self, organization1, user1):
        """Ensure a normal user can't delete an organization."""
        with self.run_requests_as(user1):
            resp = self.client.delete(f"{self.url}/{organization1.id}")
        self.assertEqual(resp.status_code, 403)

    @fixtures.use
    def test_delete_anonymous(self, organization1):
        """Ensure that an anonymous user can't delete an organization."""
        resp = self.client.delete(f"{self.url}/{organization1.id}")
        self.assertEqual(resp.status_code, 401)

    @fixtures.use
    def test_delete_not_possible_as_long_as_there_are_contacts(
        self, organization1, super_user
    ):
        """Ensure we can't delete an organization if there are contacts."""
        existing_contact = Contact(
            given_name="existing",
            family_name="contact",
            email="existing.contact@localhost",
            organization=organization1.name,
        )
        db.session.add(existing_contact)
        db.session.commit()

        with self.run_requests_as(super_user):
            resp = self.client.delete(f"{self.url}/{organization1.id}")
        self.assertEqual(resp.status_code, 409)

    @fixtures.use
    def test_patch_changes_organization_of_users(self, organization1, super_user):
        """Ensure that a patch here will update the organization entry of the associated contacts."""
        existing_contact = Contact(
            given_name="existing",
            family_name="contact",
            email="existing.contact@localhost",
            organization=organization1.name,
        )
        db.session.add(existing_contact)
        db.session.commit()

        payload = {
            "data": {
                "type": "organization",
                "id": str(organization1.id),
                "attributes": {
                    "name": "fancy new organization",
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{organization1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(resp.status_code, 200)

        reloaded_contact = (
            db.session.query(Contact).filter_by(id=existing_contact.id).first()
        )
        self.assertEqual(reloaded_contact.organization, "fancy new organization")
