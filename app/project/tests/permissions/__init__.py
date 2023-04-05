# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from project.api.models import Configuration, Contact, Device, Platform, User
from project.api.models.base_model import db
from project.tests.base import create_token, fake, generate_userinfo_data


def create_superuser_token():
    contact = Contact(
        given_name="Test",
        family_name="User",
        email="test-superuser@ufz.de",
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
        manufacturer_name=fake.company(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    db.session.add(device)
    db.session.commit()
    return device


def create_a_test_platform(
    group_ids=[],
    public=False,
    private=False,
    internal=True,
):
    platform = Platform(
        short_name=fake.pystr(),
        manufacturer_name=fake.company(),
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    db.session.add(platform)
    db.session.commit()
    return platform


def create_a_test_configuration(cfg_permission_group=None, public=False, internal=True):
    configuration = Configuration(
        label=fake.pystr(),
        is_public=public,
        is_internal=internal,
        cfg_permission_group=cfg_permission_group,
    )
    db.session.add(configuration)
    db.session.commit()
    return configuration
