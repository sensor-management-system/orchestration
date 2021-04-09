from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.tests.base import BaseTestCase, generate_token_data


class TestContactModels(BaseTestCase):
    """
    Test Contact Model
    """

    def test_add_contact_model(self):
        """""Ensure Add contact model """
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        db.session.add(contact)
        db.session.commit()

        contact = db.session.query(Contact).filter_by(id=contact.id).one()
        self.assertIn(contact.email, contact.email)
