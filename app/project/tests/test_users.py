import unittest

from project.api.models.base_model import db
from project.api.models.user import User
from project.api.schemas.user_schema import UserSchema
from project.tests.base import BaseTestCase
from project.tests.test_contacts import TestContactServices
from project.urls import base_url


class TestUsersServices(BaseTestCase):
    """
    Test User Services
    """

    user_url = base_url + "/users"
    object_type = "user"
    json_data_url = "/usr/src/app/project/tests/drafts/users_test_data.json"

    def test_add_user_model(self):
        """""Ensure Add platform model """
        contact = TestContactServices().test_add_contact_model()
        user = User(id=445, subject="test_user@test.test", contact_id=contact.id)
        UserSchema().dump(user)
        db.session.add(user)
        db.session.commit()

        u = db.session.query(User).filter_by(id=user.id).one()
        self.assertIn(u.subject, user.subject)


if __name__ == "__main__":
    unittest.main()
