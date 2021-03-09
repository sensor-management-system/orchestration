import unittest

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.tests.base import BaseTestCase, generate_token_data


class TestContactModels(BaseTestCase):
    """
    Test Contact Model
    """

    def test_add_contact_model(self):
        """""Ensure Add contact model """
        jwt1 = generate_token_data()
        c = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        db.session.add(c)
        db.session.commit()

        c = db.session.query(Contact).filter_by(id=c.id).one()
        self.assertIn(c.email, c.email)


if __name__ == "__main__":
    unittest.main()
