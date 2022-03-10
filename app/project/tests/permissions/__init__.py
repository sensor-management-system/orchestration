from project.api.models import Contact, User, Device
from project.api.models.base_model import db
from project.tests.base import create_token
from project.tests.base import fake
from project.tests.base import generate_userinfo_data

from project.api.models import Platform


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


def create_a_test_contact(userinfo=None):
    if not userinfo:
        userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add(contact)
    db.session.commit()
    return contact


def create_a_test_device(group_ids=[], public=False, private=False, internal=True):
    device = Device(
        short_name=fake.pystr(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    db.session.add(device)
    db.session.commit()
    return device


def create_a_test_platform(group_ids=[], public=False, private=False, internal=True, ):
    platform = Platform(
        short_name=fake.pystr(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    db.session.add(platform)
    db.session.commit()
    return platform
