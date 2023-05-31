# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test cases for the CLI commands."""

import json
import os
import sys
import tempfile
from contextlib import contextmanager

from click.testing import CliRunner

from manage import deactivate_a_user, loaddata, reactivate_a_user
from project import db
from project.api.models import Contact, Device, TsmEndpoint, User
from project.tests.base import BaseTestCase, fake

# import manage packages onto the path

sys.path.append(os.path.abspath(os.path.join("..", "manage")))


# Avoid DetachedInstanceError in Flask-SQLAlchemy
# https://stackoverflow.com/a/51452451
@contextmanager
def no_expire():
    """Allow us to use the share the session between test code & cli runner."""
    s = db.session()
    s.expire_on_commit = False
    try:
        yield
    finally:
        s.expire_on_commit = True


class TestCliCommands(BaseTestCase):
    """Test class for some of the CLI commands."""

    def test_deactivate_a_user_with_no_substituted_user(self):
        """Ensure that a user can be deactivated and all it data are changed to deactivation message."""
        with no_expire():
            contact = Contact(
                given_name="Test",
                family_name="User1",
                email="test.user1@ufz.test",
            )
            user = User(subject="testuser1@ufz.test", contact=contact)

            db.session.add_all([contact, user])
            db.session.commit()

            runner = CliRunner()
            result = runner.invoke(
                deactivate_a_user, ["testuser1@ufz.test"], env={"FLASK_APP": "manage"}
            )
            assert not result.exception
            assert result.exit_code == 0
            assert user.active is False
            assert contact.email == f"User {user.id} is deactivated"

    def test_deactivate_a_user_with_substituted_user(self):
        """Ensure that a user can be deactivated and provide a substituted user."""
        with no_expire():
            contact1 = Contact(
                given_name="Test",
                family_name="User1",
                email="test.user1@ufz.test",
            )
            contact2 = Contact(
                given_name="Test",
                family_name="User2",
                email="test.user2@ufz.test",
            )
            user1 = User(subject="testuser1@ufz.test", contact=contact1)
            user2 = User(subject="testuser2@ufz.test", contact=contact2)
            device = Device(
                short_name="device_short_name test",
                created_by_id=user1.id,
                manufacturer_name=fake.company(),
                is_public=False,
                is_private=False,
                is_internal=True,
            )

            db.session.add_all([contact1, contact2, user1, user2, device])
            device.contacts.append(contact1)
            db.session.commit()

            runner = CliRunner()
            result = runner.invoke(
                deactivate_a_user,
                ["testuser1@ufz.test", "--dest-user-subject=testuser2@ufz.test"],
                env={"FLASK_APP": "manage"},
            )

            assert not result.exception
            assert result.exit_code == 0
            assert user1.active is False
            assert user2.active is True
            assert len(device.contacts) == 2

    def test_reactivate_a_user(self):
        """Ensure that a user can be reactivated."""
        with no_expire():
            contact = Contact(
                given_name="User is deactivated",
                family_name="User is deactivated",
                email="User is deactivated",
                active=False,
            )
            user = User(subject="testuser@ufz.test", contact=contact, active=False)
            db.session.expire_on_commit = False
            db.session.add_all([contact, user])
            db.session.commit()

            runner = CliRunner()

            reactivate = runner.invoke(
                reactivate_a_user,
                ["testuser@ufz.test"],
                env={"FLASK_APP": "manage"},
                input="Test\nUser\ntest.user@ufz.test\n",
            )
            assert user.active is True
            assert contact.active is True
            assert contact.email == "test.user@ufz.test"
            assert reactivate.exit_code == 0

    def test_load_data_completely_new(self):
        """Ensure we can insert completly new data."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            data = [
                {
                    "fields": {
                        "name": "FOO",
                        "url": "https://foo",
                    },
                    "model": "TsmEndpoint",
                    "pk": 1,
                },
                {
                    "fields": {
                        "name": "BAR",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "pk": 2,
                },
            ]
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(2, db.session.query(TsmEndpoint).count())
            tsm_endpoint1 = db.session.get(TsmEndpoint, 1)
            tsm_endpoint2 = db.session.get(TsmEndpoint, 2)
            self.assertEqual(tsm_endpoint1.name, "FOO")
            self.assertEqual(tsm_endpoint1.url, "https://foo")
            self.assertEqual(tsm_endpoint2.name, "BAR")
            self.assertEqual(tsm_endpoint2.url, "https://bar")

    def test_load_data_update_existing(self):
        """Ensure we can update existing data."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            tsm_endpoint = TsmEndpoint(id=1, name="foo", url="https://foo")
            db.session.add(tsm_endpoint)
            db.session.commit()
            data = [
                {
                    "fields": {
                        "name": "BAR",
                        "url": "https://bar",
                    },
                    "model": "TsmEndpoint",
                    "pk": 1,
                },
            ]
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(1, db.session.query(TsmEndpoint).count())
            reloaded_tsm_endpoint = db.session.get(TsmEndpoint, 1)
            self.assertEqual(reloaded_tsm_endpoint.name, "BAR")
            self.assertEqual(reloaded_tsm_endpoint.url, "https://bar")

    def test_load_data_empty_data(self):
        """Ensure we can run it without any data in it."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            data = []
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                json.dump(data, temp_file)
                path = temp_file.name
                temp_file.flush()
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
            self.assertEqual(result.exit_code, 0)

            self.assertEqual(0, db.session.query(TsmEndpoint).count())

    def test_load_data_empty_file_error(self):
        """Ensure we raise an error if we try to load a completly empty file."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path],
                    env={"FLASK_APP": "manage"},
                )
                self.assertTrue(isinstance(result.exception, json.JSONDecodeError))

    def test_load_data_missing_file_error(self):
        """Ensure we raise an error if there is no such file."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                different_path = path + "123432432432423543543.json"
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [different_path],
                    env={"FLASK_APP": "manage"},
                )
                self.assertTrue(isinstance(result.exception, FileNotFoundError))

    def test_load_data_empty_file_ignore(self):
        """Ensure we can ignore it if the file is completely empty."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [path, "--skip-empty-file"],
                    env={"FLASK_APP": "manage"},
                )
                self.assertEqual(result.exit_code, 0)

    def test_load_data_missing_file_ignore(self):
        """Ensure we can ignore it if the file doesn't exists."""
        with no_expire():
            self.assertEqual(0, db.session.query(TsmEndpoint).count())
            with tempfile.NamedTemporaryFile(mode="w+t") as temp_file:
                path = temp_file.name
                different_path = path + "123432432432423543543.json"
                runner = CliRunner()
                result = runner.invoke(
                    loaddata,
                    [different_path, "--skip-missing-file"],
                    env={"FLASK_APP": "manage"},
                )
                self.assertEqual(result.exit_code, 0)
