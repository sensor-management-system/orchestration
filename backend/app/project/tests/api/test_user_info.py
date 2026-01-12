# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test classes & functions for the userinfo endpoint."""
import datetime
import json

from project import base_url
from project.api.models import Contact, PermissionGroup, PermissionGroupMembership, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, Fixtures

fixtures = Fixtures()


@fixtures.register("group1", scope=lambda: db.session)
def create_group1():
    """Create a permission group."""
    result = PermissionGroup(name="group1", entitlement="group1")
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("group2", scope=lambda: db.session)
def create_group2():
    """Create another permission group."""
    result = PermissionGroup(name="group2", entitlement="group2")
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


@fixtures.register("membership_of_user1_in_group1", scope=lambda: db.session)
@fixtures.use(["user1", "group1"])
def create_membership_of_user1_in_group1(user1, group1):
    """Create a permission group."""
    result = PermissionGroupMembership(user=user1, permission_group=group1)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("membership_of_user1_in_group2", scope=lambda: db.session)
@fixtures.use(["user1", "group2"])
def create_membership_of_user1_in_group2(user1, group2):
    """Create a permission group."""
    result = PermissionGroupMembership(user=user1, permission_group=group2)
    db.session.add(result)
    db.session.commit()
    return result


class TestUserinfo(BaseTestCase):
    """Tests for the user info endpoint."""

    url = base_url + "/user-info"

    def test_get_without_jwt(self):
        """Ensure the GET /user-info route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    @fixtures.use
    def test_get_with_user_not_assigned_to_any_permission_group(self, user1):
        """Ensure response with an empty list if user not assigned to any permission group."""
        with self.run_requests_as(user1):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["member"], [])

    @fixtures.use
    def test_get_with_user_is_assigned_to_permission_groups(
        self,
        user1,
        group1,
        group2,
        membership_of_user1_in_group1,
        membership_of_user1_in_group2,
    ):
        """Ensure response with an empty list if user not assigned to any permission group."""
        with self.run_requests_as(user1):
            response = self.client.get(
                f"{self.url}?include=device,contact,parent_platform,configuration",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["member"], [str(group1.id), str(group2.id)])

    @fixtures.use
    def test_post_not_allowed(self, user1):
        """Ensure post request not allowed."""
        data = {}
        with self.run_requests_as(user1):
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 405)
        data = response.json
        self.assertEqual(data["errors"][0]["source"], "endpoint is readonly")

    @fixtures.use
    def test_get_includes_apikey(self, user1):
        """Test that we include the apikey in the payload."""
        user1.apikey = "1234"
        db.session.add_all([user1])
        db.session.commit()
        with self.run_requests_as(user1):
            response = self.client.get(
                self.url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["apikey"], "1234")
        # And we check that we use the export control setting.
        self.assertEqual(
            response.json["data"]["attributes"]["is_export_control"], False
        )

    @fixtures.use
    def test_get_includes_export_control(self, user1):
        """Test that we include the export control in the payload."""
        user1.is_export_control = True

        db.session.add_all([user1])
        db.session.commit()

        with self.run_requests_as(user1):
            response = self.client.get(
                self.url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["is_export_control"], True)

    @fixtures.use
    def test_get_includes_contact_id(self, user1):
        """Test that we include the contact id in the payload."""
        with self.run_requests_as(user1):
            response = self.client.get(
                self.url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["data"]["relationships"]["contact"]["data"]["id"],
            str(user1.contact.id),
        )

    @fixtures.use
    def test_get_id_is_string(self, user1):
        """Test that the id is of type string."""
        with self.run_requests_as(user1):
            response = self.client.get(
                self.url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(user1.id))

    @fixtures.use
    def test_get_includes_subject(self, user1):
        """Ensure we also give out the subject in the payload."""
        with self.run_requests_as(user1):
            response = self.client.get(
                self.url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["subject"], "dummy")

    @fixtures.use
    def test_get_includes_terms_of_use_agreement_date(self, user1):
        """Ensure that we give out the agreement date in the payload."""
        user1.terms_of_use_agreement_date = datetime.datetime(
            2023, 2, 28, 12, 0, 0, tzinfo=datetime.timezone.utc
        )
        db.session.add_all([user1])
        db.session.commit()
        with self.run_requests_as(user1):
            response = self.client.get(
                self.url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["data"]["attributes"]["terms_of_use_agreement_date"],
            "2023-02-28T12:00:00+00:00",
        )

    @fixtures.use
    def test_get_includes_terms_of_use_agreement_date_not_set(self, user1):
        """Ensure that we give out the null agreement date (not set yet)."""
        user1.terms_of_use_agreement_date = None
        db.session.add_all([user1])
        db.session.commit()
        with self.run_requests_as(user1):
            response = self.client.get(
                self.url,
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["data"]["attributes"]["terms_of_use_agreement_date"], None
        )
