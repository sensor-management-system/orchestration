from project.api.models import Contact
from project.api.models.base_model import db
from project.api.models.user import User
from project.tests.base import BaseTestCase, generate_userinfo_data


class TestUsersModel(BaseTestCase):
    """
    Test User Services
    """

    def test_add_user_model(self):
        """""Ensure Add user model """
        userinfo = generate_userinfo_data()
        c = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(id=445, subject="test_user@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        u = db.session.query(User).filter_by(id=user.id).one()
        self.assertIn(u.subject, user.subject)
