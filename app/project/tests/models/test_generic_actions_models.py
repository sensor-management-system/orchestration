from datetime import datetime

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.models.device import Device
from project.api.models.generic_actions import (
    GenericConfigurationAction,
    GenericDeviceAction,
    GenericPlatformAction,
)
from project.api.models.platform import Platform
from project.api.models.user import User
from project.tests.base import BaseTestCase, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model


def generate_platform_action_model(public=True, private=False, internal=False):
    platform = Platform(
        short_name="short_name test",
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    mock_jwt = generate_token_data()
    contact = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    u = User(subject=mock_jwt["sub"], contact=contact)
    generic_platform_action = GenericPlatformAction(
        description="test GenericPlatformAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=datetime.now(),
        end_date=None,
        created_by=u,
    )
    generic_platform_action.contact = contact
    generic_platform_action.platform = platform
    db.session.add_all([platform, contact, u, generic_platform_action])
    db.session.commit()
    return generic_platform_action


def generate_device_action_model(public=True, private=False, internal=False):
    d = Device(
        short_name="test device", is_public=public, is_private=private, is_internal=internal,
    )

    mock_jwt = generate_token_data()
    c1 = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )

    u1 = User(subject=mock_jwt["sub"], contact=c1)

    generic_device_action = GenericDeviceAction(
        description="test GenericDeviceAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=datetime.now(),
        end_date=None,
        created_by=u1,
    )
    generic_device_action.contact = c1
    generic_device_action.device = d
    db.session.add_all([d, c1, u1, generic_device_action])
    db.session.commit()
    return generic_device_action


def generate_configuration_action_model():
    config = generate_configuration_model()
    mock_jwt = generate_token_data()
    c1 = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    u1 = User(subject=mock_jwt["sub"], contact=c1)

    generic_configuration_action = GenericConfigurationAction(
        description="test GenericConfigurationAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=datetime.now(),
        end_date=None,
        created_by=u1,
    )
    generic_configuration_action.contact = c1
    generic_configuration_action.configuration = config
    db.session.add_all([config, c1, u1, generic_configuration_action])
    db.session.commit()
    return generic_configuration_action


class TestGenericActions(BaseTestCase):
    """
    Test Generic Actions
    """

    def test_add_generic_platform_action_model(self):
        """""Ensure Add generic platform action model """
        platform_action_model = generate_platform_action_model()
        generic_platform_action = (
            db.session.query(GenericPlatformAction)
            .filter_by(action_type_name="testing")
            .one()
        )
        self.assertDictEqual(
            platform_action_model.__dict__, generic_platform_action.__dict__
        )

    def test_add_generic_device_action_model(self):
        """""Ensure Add generic device action model """
        device_action_model = generate_device_action_model()
        generic_device_action = (
            db.session.query(GenericDeviceAction)
            .filter_by(action_type_name="testing")
            .one()
        )
        self.assertDictEqual(
            device_action_model.__dict__, generic_device_action.__dict__
        )

    def test_add_generic_configuration_action_model(self):
        """""Ensure Add generic configuration action model """
        configuration_action_model = generate_configuration_action_model()
        generic_configuration_action = (
            db.session.query(GenericConfigurationAction)
            .filter_by(action_type_name="testing")
            .one()
        )
        self.assertDictEqual(
            configuration_action_model.__dict__, generic_configuration_action.__dict__
        )
