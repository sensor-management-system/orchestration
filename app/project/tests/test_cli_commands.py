import os
import sys
from contextlib import contextmanager

from click.testing import CliRunner
from manage import deactivate_a_user, reactivate_a_user
from project import db
from project.api.models import Device
from project.api.models import User, Contact
from project.tests.base import BaseTestCase

# import manage packages onto the path
sys.path.append(os.path.abspath(os.path.join('..', 'manage')))


# Avoid DetachedInstanceError in Flask-SQLAlchemy
# https://stackoverflow.com/a/51452451
@contextmanager
def no_expire():
    s = db.session()
    s.expire_on_commit = False
    try:
        yield
    finally:
        s.expire_on_commit = True


class TestCliCommands(BaseTestCase):

    def test_deactivate_a_user_with_no_substituted_user(self):
        """Ensure that a user can be deactivated and all it
        data are changed to deactivation message."""
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
            result = runner.invoke(deactivate_a_user, ["testuser1@ufz.test"],
                                   env={"FLASK_APP": "manage"})
            assert not result.exception
            assert result.exit_code == 0
            assert user.active is False
            assert contact.email == f"User {user.id} is deactivated"

    def test_deactivate_a_user_with_substituted_user(self):
        """Ensure that a user can be deactivated and provide
        a substituted user."""
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
            device = Device(short_name="device_short_name test", created_by_id=user1.id)

            db.session.add_all([contact1, contact2, user1, user2, device])
            device.contacts.append(contact1)
            db.session.commit()

            runner = CliRunner()
            result = runner.invoke(deactivate_a_user, ["testuser1@ufz.test", "--dest-user-subject=testuser2@ufz.test"],
                                   env={"FLASK_APP": "manage"})

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
                active=False
            )
            user = User(subject="testuser@ufz.test", contact=contact, active=False)
            db.session.expire_on_commit = False
            db.session.add_all([contact, user])
            db.session.commit()

            runner = CliRunner()

            reactivate = runner.invoke(reactivate_a_user, ["testuser@ufz.test"], env={"FLASK_APP": "manage"},
                                       input="Test\nUser\ntest.user@ufz.test\n")
            assert user.active is True
            assert contact.active is True
            assert contact.email == "test.user@ufz.test"
            assert reactivate.exit_code == 0
