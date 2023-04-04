"""Tests for the sites."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Site, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestSites(BaseTestCase):
    """Test class for the site permission management."""

    url = base_url + "/sites"

    def test_patch_to_different_permission_group(self):
        """Ensure we can't update to a permission group we aren't members."""
        site = Site(
            label="test site", is_public=False, is_internal=True, group_ids=["1"]
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
        db.session.add_all([site, contact, user])
        db.session.commit()

        payload = {
            "data": {
                "type": "site",
                "id": site.id,
                "attributes": {
                    "group_ids": ["2"],
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*site.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{site.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_remove_permission_group_non_admin(self):
        """Ensure we can't remove a permission group we aren't admins."""
        site = Site(
            label="test site", is_public=False, is_internal=True, group_ids=["1"]
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
        db.session.add_all([site, contact, user])
        db.session.commit()

        payload = {
            "data": {
                "type": "site",
                "id": site.id,
                "attributes": {
                    "group_ids": ["2"],
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*site.group_ids, "2"],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{site.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
