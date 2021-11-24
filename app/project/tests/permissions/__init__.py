from project.api.models.base_model import db
from project.api.models import Contact, User
from project.tests.base import create_token


def create_superuser_token():
    contact = Contact(
        given_name="Test", family_name="User", email="test-superuser@ufz.de",
    )
    user = User(subject="superuser@test.test", contact=contact, is_superuser=True)
    db.session.add_all([contact, user])
    db.session.commit()
    token_data = {
        "sub": user.subject,
        "iss": "SMS unittest",
        "family_name": contact.family_name,
        "given_name": contact.given_name,
        "email": contact.email,
        "aud": "SMS",
    }
    access_headers = create_token(token_data)
    return access_headers