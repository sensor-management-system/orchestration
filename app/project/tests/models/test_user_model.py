import unittest

from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.api.models.user import User
from project.tests.base import BaseTestCase, generate_token_data


class TestUsersModel(BaseTestCase):
    """
    Test User Services
    """

    user_url = base_url + "/users"
    object_type = "user"
    json_data_url = "/usr/src/app/project/tests/drafts/users_test_data.json"

    def test_add_user_model(self):
        """""Ensure Add user model """
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        user = User(id=445, subject="test_user@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        u = db.session.query(User).filter_by(id=user.id).one()
        self.assertIn(u.subject, user.subject)


if __name__ == "__main__":
    unittest.main()
