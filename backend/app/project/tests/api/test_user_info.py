# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test classes & functions for the userinfo endpoint."""
import datetime
import json
from unittest import skipIf
from unittest.mock import patch

import pytz
from flask import current_app

from project import base_url
from project.api.models import Contact, User
from project.api.models.base_model import db
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestUserinfo(BaseTestCase):
    """Tests for the user info endpoint."""

    url = base_url + "/user-info"

    def test_get_without_jwt(self):
        """Ensure the GET /user-info route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    @skipIf(
        not current_app.config["IDL_URL"],
        "will not work without idl url configuration.",
    )
    def test_get_with_jwt_user_not_assigned_to_any_permission_group(self):
        """Ensure response with an empty list if user not assigned to any permission group."""
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["admin"], [])
        self.assertEqual(data["attributes"]["member"], [])

    def test_get_with_jwt_user_is_assigned_to_permission_groups(self):
        """Ensure response with an empty list if user not assigned to any permission group."""
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.get(
                    f"{self.url}?include=device,contact,parent_platform,configuration",
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["admin"], ["1"])
        self.assertEqual(data["attributes"]["member"], ["2", "3"])

    def test_post_not_allowed(self):
        """Ensure post request not allowed."""
        access_headers = create_token()
        data = {}
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 405)
        data = response.json
        self.assertEqual(data["errors"][0]["source"], "endpoint is readonly")

    def test_get_includes_apikey(self):
        """Test that we include the apikey in the payload."""
        contact = Contact(given_name="A", family_name="B", email="ab@localhost")
        user = User(subject="dummy", contact=contact, apikey="1234")
        db.session.add_all([contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups_for_a_user:
                test_get_all_permission_groups_for_a_user.return_value = (
                    IDL_USER_ACCOUNT
                )
                with self.client:
                    response = self.client.get(
                        self.url,
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["apikey"], "1234")
        # And we check that we use the export control setting.
        self.assertEqual(
            response.json["data"]["attributes"]["is_export_control"], False
        )

    def test_get_includes_export_control(self):
        """Test that we include the export control in the payload."""
        contact = Contact(given_name="A", family_name="B", email="ab@localhost")
        user = User(subject="dummy", contact=contact, is_export_control=True)
        db.session.add_all([contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups_for_a_user:
                test_get_all_permission_groups_for_a_user.return_value = (
                    IDL_USER_ACCOUNT
                )
                with self.client:
                    response = self.client.get(
                        self.url,
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["is_export_control"], True)

    def test_get_includes_contact_id(self):
        """Test that we include the contact id in the payload."""
        contact = Contact(given_name="A", family_name="B", email="ab@localhost")
        user = User(subject="dummy", contact=contact)
        db.session.add_all([contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups_for_a_user:
                test_get_all_permission_groups_for_a_user.return_value = (
                    IDL_USER_ACCOUNT
                )
                with self.client:
                    response = self.client.get(
                        self.url,
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["data"]["relationships"]["contact"]["data"]["id"],
            str(contact.id),
        )

    def test_get_id_is_string(self):
        """Test that we the id is of type string."""
        contact = Contact(given_name="A", family_name="B", email="ab@localhost")
        user = User(subject="dummy", contact=contact)
        db.session.add_all([contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups_for_a_user:
                test_get_all_permission_groups_for_a_user.return_value = (
                    IDL_USER_ACCOUNT
                )
                with self.client:
                    response = self.client.get(
                        self.url,
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["id"], str(user.id))

    def test_get_includes_subject(self):
        """Ensure we also give out the subject in the payload."""
        contact = Contact(given_name="A", family_name="B", email="ab@localhost")
        user = User(subject="dummy", contact=contact)
        db.session.add_all([contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups_for_a_user:
                test_get_all_permission_groups_for_a_user.return_value = (
                    IDL_USER_ACCOUNT
                )
                with self.client:
                    response = self.client.get(
                        self.url,
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["subject"], "dummy")

    def test_get_includes_terms_of_use_agreement_date(self):
        """Ensure that we give out the agreement date in the payload."""
        contact = Contact(given_name="A", family_name="B", email="ab@localhost")
        user = User(
            subject="dummy",
            contact=contact,
            terms_of_use_agreement_date=datetime.datetime(
                2023, 2, 28, 12, 0, 0, tzinfo=pytz.utc
            ),
        )
        db.session.add_all([contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups_for_a_user:
                test_get_all_permission_groups_for_a_user.return_value = (
                    IDL_USER_ACCOUNT
                )
                with self.client:
                    response = self.client.get(
                        self.url,
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["data"]["attributes"]["terms_of_use_agreement_date"],
            "2023-02-28T12:00:00+00:00",
        )

    def test_get_includes_terms_of_use_agreement_date_not_set(self):
        """Ensure that we give out the null agreement date (not set yet)."""
        contact = Contact(given_name="A", family_name="B", email="ab@localhost")
        user = User(subject="dummy", contact=contact, terms_of_use_agreement_date=None)
        db.session.add_all([contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups_for_a_user:
                test_get_all_permission_groups_for_a_user.return_value = (
                    IDL_USER_ACCOUNT
                )
                with self.client:
                    response = self.client.get(
                        self.url,
                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["data"]["attributes"]["terms_of_use_agreement_date"], None
        )
