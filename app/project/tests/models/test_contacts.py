from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.tests.base import BaseTestCase, generate_userinfo_data


class TestContactModels(BaseTestCase):
    """
    Test Contact Model
    """

    def test_add_contact_model(self):
        """""Ensure Add contact model """
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add(contact)
        db.session.commit()

        contact = db.session.query(Contact).filter_by(id=contact.id).one()
        self.assertIn(contact.email, contact.email)
