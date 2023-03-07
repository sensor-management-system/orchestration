"""Test classes & functions for making changes on the user model."""

import datetime
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import Contact, User
from project.api.models.base_model import db
from project.api.resources.user_modification import AcceptTermsOfUse
from project.tests.base import BaseTestCase


class TestRevokeApikey(BaseTestCase):
    """Test cases to revoke the apikey."""

    url = base_url + "/revoke-apikey"

    def test_post_without_user(self):
        """Ensure that we need a user, return 401 otherwise."""
        response = self.client.post(self.url, content_type="application/vnd.api+json")
        self.assertEqual(response.status_code, 401)

    def test_post_with_user(self):
        """Ensure that we get a new apikey if we revoke the current one."""
        contact = Contact(
            given_name="Luke",
            family_name="Skzwalker",
            email="son.of.vader@rebellion.base",
        )
        old_apikey = "12345"
        user = User(subject="son.of.vader", contact=contact, apikey=old_apikey)

        db.session.add_all([contact, user])
        db.session.commit()

        user_id = user.id
        with self.run_requests_as(user):
            response = self.client.post(
                self.url, content_type="application/vnd.api+json"
            )
            self.assertEqual(response.status_code, 200)
            data = response.json
            new_apikey = data["data"]["attributes"]["apikey"]
            self.assertFalse(new_apikey == old_apikey)

        reloaded_user = db.session.query(User).filter_by(id=user_id).one()
        self.assertEqual(reloaded_user.apikey, new_apikey)

    def test_get(self):
        """Ensure that the get method is not allowed for this endpoint."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


class TestAcceptTermsOfUse(BaseTestCase):
    """Test cases to agree the terms of use."""

    url = base_url + "/accept-terms-of-use"

    def test_post_without_user(self):
        """Ensure that we need a user, return 401 otherwise."""
        response = self.client.post(self.url, content_type="application/vnd.api+json")
        self.assertEqual(response.status_code, 401)

    def test_post_with_user(self):
        """Ensure that we update the terms of use agreement date."""
        contact = Contact(
            given_name="Luke",
            family_name="Skzwalker",
            email="son.of.vader@rebellion.base",
        )
        user = User(
            subject="son.of.vader", contact=contact, terms_of_use_agreement_date=None
        )

        db.session.add_all([contact, user])
        db.session.commit()

        user_id = user.id

        new_aggreement_date = datetime.datetime(2023, 2, 28, 12, 0, 0, tzinfo=pytz.utc)
        with self.run_requests_as(user):
            with patch.object(AcceptTermsOfUse, "get_current_time") as mock:
                mock.return_value = new_aggreement_date
                response = self.client.post(
                    self.url, content_type="application/vnd.api+json"
                )
            self.assertEqual(response.status_code, 200)
            data = response.json
            new_date = data["data"]["attributes"]["terms_of_use_agreement_date"]
            self.assertEqual(new_date, "2023-02-28T12:00:00+00:00")

        reloaded_user = db.session.query(User).filter_by(id=user_id).one()
        self.assertEqual(reloaded_user.terms_of_use_agreement_date, new_aggreement_date)

    def test_get(self):
        """Ensure that the get method is not allowed for this endpoint."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
