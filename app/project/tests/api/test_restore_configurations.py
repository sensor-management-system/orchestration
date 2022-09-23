"""Tests for the restoring configurations."""

from unittest.mock import patch

from project import base_url
from project.api.models import Configuration, Contact, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestRestoreConfigurations(BaseTestCase):
    """Test class to restore configurations."""

    configurations_url = base_url + "/configurations"

    def setUp(self):
        """Set up some data to test with."""
        super().setUp()

        contact1 = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        contact2 = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.normal_user = User(subject=contact1.email, contact=contact1)
        self.super_user = User(
            subject=contact2.email, contact=contact2, is_superuser=True
        )
        self.configuration = Configuration(
            label="archived configuration",
            is_public=True,
            is_internal=False,
            archived=True,
            update_description="create;basic data",
        )
        db.session.add_all(
            [
                contact1,
                contact2,
                self.normal_user,
                self.super_user,
                self.configuration,
            ]
        )
        db.session.commit()

    def test_get(self):
        """Ensure that it is not allowed to use the get method."""
        response = self.client.get(f"{self.configurations_url}/12345/restore")
        self.assertEqual(response.status_code, 405)

    def test_post_unauthorized(self):
        """Ensure that we don't allow anonymous to restore."""
        response = self.client.post(f"{self.configurations_url}/12345/restore")
        self.assertEqual(response.status_code, 401)

    def test_post_nonexisting(self):
        """Ensure that we got an 404 when the configuration doesn't exist."""
        with self.run_requests_as(self.normal_user):
            response = self.client.post(f"{self.configurations_url}/12345/restore")
        self.assertEqual(response.status_code, 404)

    def test_post_user_not_in_idl(self):
        """Ensure that an ordinary user without an entry in the idl can't restore."""
        self.configuration.cfg_permission_group = "123"
        db.session.add(self.configuration)
        db.session.commit()

        with patch.object(
            idl, "get_all_permission_groups_for_a_user", return_value=None
        ):
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.configuration.id}/restore"
                )
        self.assertEqual(response.status_code, 403)

    def test_post_user_not_in_any_group(self):
        """Ensure that an ordinary user without group membership can't restore."""
        self.configuration.cfg_permission_group = "123"
        db.session.add(self.configuration)
        db.session.commit()

        with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
            mock.return_value = UserAccount(
                id="1000",
                username=self.normal_user.subject,
                administrated_permission_groups=[],
                membered_permission_groups=[],
            )
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.configuration.id}/restore"
                )
        self.assertEqual(response.status_code, 403)

    def test_post_user_in_a_group(self):
        """Ensure that an ordinary user can't restore."""
        self.configuration.cfg_permission_group = "123"
        db.session.add(self.configuration)
        db.session.commit()

        with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
            mock.return_value = UserAccount(
                id="1000",
                username=self.normal_user.subject,
                administrated_permission_groups=[],
                membered_permission_groups=["123"],
            )
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.configuration.id}/restore"
                )
        self.assertEqual(response.status_code, 403)

    def test_post_admin_in_a_group(self):
        """Ensure that we can unset the archived flag as admins."""
        self.configuration.cfg_permission_group = "123"
        db.session.add(self.configuration)
        db.session.commit()

        with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
            mock.return_value = UserAccount(
                id="1000",
                username=self.normal_user.subject,
                administrated_permission_groups=["123"],
                membered_permission_groups=[],
            )
            with self.run_requests_as(self.normal_user):
                response = self.client.post(
                    f"{self.configurations_url}/{self.configuration.id}/restore"
                )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=self.configuration.id).one()
        )
        self.assertFalse(reloaded_configuration.archived)
        self.assertEqual(
            reloaded_configuration.update_description, "restore;basic data"
        )
        self.assertEqual(reloaded_configuration.updated_by_id, self.normal_user.id)

    def test_post_superuser(self):
        """Ensure that we can unset the archived flag super user."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.configuration.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=self.configuration.id).one()
        )
        self.assertFalse(reloaded_configuration.archived)
        self.assertEqual(
            reloaded_configuration.update_description, "restore;basic data"
        )
        self.assertEqual(reloaded_configuration.updated_by_id, self.super_user.id)

    def test_post_already_restored(self):
        """Ensure that it doesn't matter if the configuration is not archived at the beginning."""
        self.configuration.archived = False
        db.session.add(self.configuration)
        db.session.commit()

        with self.run_requests_as(self.super_user):
            response = self.client.post(
                f"{self.configurations_url}/{self.configuration.id}/restore"
            )
        self.assertEqual(response.status_code, 204)
        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=self.configuration.id).one()
        )
        self.assertFalse(reloaded_configuration.archived)
        # But we don't change the entity
        self.assertEqual(reloaded_configuration.update_description, "create;basic data")
        self.assertIsNone(reloaded_configuration.updated_by_id)
