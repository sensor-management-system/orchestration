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


def generate_platform_action_model():
    p = Platform(
        short_name="short_name test",
    )
    jwt1 = generate_token_data()
    c = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )
    u = User(subject=jwt1["sub"], contact=c)
    gpa = GenericPlatformAction(
        description="test GenericPlatformAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=datetime.now(),
        end_date=None,
        created_by=u,
    )
    gpa.contact = c
    gpa.platform = p
    db.session.add_all([p, c, u, gpa])
    db.session.commit()
    return gpa


def generate_device_action_model():
    d = Device(
        short_name="test device",
    )

    jwt1 = generate_token_data()
    c1 = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )

    u1 = User(subject=jwt1["sub"], contact=c1)

    gpa = GenericDeviceAction(
        description="test GenericDeviceAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=datetime.now(),
        end_date=None,
        created_by=u1,
    )
    gpa.contact = c1
    gpa.device = d
    db.session.add_all([d, c1, u1, gpa])
    db.session.commit()
    return gpa


def generate_configuration_action_model():
    config = generate_configuration_model()
    jwt1 = generate_token_data()
    c1 = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )
    u1 = User(subject=jwt1["sub"], contact=c1)

    gpa = GenericConfigurationAction(
        description="test GenericConfigurationAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=datetime.now(),
        end_date=None,
        created_by=u1,
    )
    gpa.contact = c1
    gpa.configuration = config
    db.session.add_all([config, c1, u1, gpa])
    db.session.commit()
    return gpa


class TestGenericActions(BaseTestCase):
    """
    Test Generic Actions
    """

    def test_add_generic_platform_action_model(self):
        """""Ensure Add generic platform action model """
        gpa = generate_platform_action_model()
        gpa_r = (
            db.session.query(GenericPlatformAction)
                .filter_by(action_type_name="testing")
                .one()
        )
        self.assertDictEqual(gpa.__dict__, gpa_r.__dict__)

    def test_add_generic_device_action_model(self):
        """""Ensure Add generic device action model """
        gpa = generate_device_action_model()
        gpa_r = (
            db.session.query(GenericDeviceAction)
                .filter_by(action_type_name="testing")
                .one()
        )
        self.assertDictEqual(gpa.__dict__, gpa_r.__dict__)

    def test_add_generic_configuration_action_model(self):
        """""Ensure Add generic configuration action model """
        gpa = generate_configuration_action_model()
        gpa_r = (
            db.session.query(GenericConfigurationAction)
                .filter_by(action_type_name="testing")
                .one()
        )
        self.assertDictEqual(gpa.__dict__, gpa_r.__dict__)
