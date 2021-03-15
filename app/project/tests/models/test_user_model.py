from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.api.models.user import User
from project.tests.base import BaseTestCase, generate_token_data


class TestUsersModel(BaseTestCase):
    """
    Test User Services
    """

    def test_add_user_model(self):
        """""Ensure Add user model """
        mock_jwt = generate_token_data()
        c = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        user = User(id=445, subject="test_user@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        u = db.session.query(User).filter_by(id=user.id).one()
        self.assertIn(u.subject, user.subject)
