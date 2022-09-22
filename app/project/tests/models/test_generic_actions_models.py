"""Tests for the generic action models."""

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.models.device import Device
from project.api.models.generic_actions import (
    GenericConfigurationAction,
    GenericDeviceAction,
    GenericPlatformAction,
)
from project.api.models.mixin import utc_now
from project.api.models.platform import Platform
from project.api.models.user import User
from project.tests.base import BaseTestCase, generate_userinfo_data
from project.tests.models.test_configurations_model import generate_configuration_model


def generate_platform_action_model(
    public=True, private=False, internal=False, group_ids=None
):
    """Generate a generic platform action instance."""
    if not group_ids:
        group_ids = []
    platform = Platform(
        short_name="short_name test",
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    u = User(subject=userinfo["sub"], contact=contact)
    generic_platform_action = GenericPlatformAction(
        description="test GenericPlatformAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=utc_now(),
        end_date=None,
        created_by=u,
    )
    generic_platform_action.contact = contact
    generic_platform_action.platform = platform
    db.session.add_all([platform, contact, u, generic_platform_action])
    db.session.commit()
    return generic_platform_action


def generate_device_action_model(
    public=True, private=False, internal=False, group_ids=None
):
    """Generate a generic device action model."""
    if not group_ids:
        group_ids = []
    d = Device(
        short_name="test device",
        is_public=public,
        is_private=private,
        is_internal=internal,
        group_ids=group_ids,
    )

    userinfo = generate_userinfo_data()
    c1 = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )

    u1 = User(subject=userinfo["sub"], contact=c1)

    generic_device_action = GenericDeviceAction(
        description="test GenericDeviceAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=utc_now(),
        end_date=None,
        created_by=u1,
    )
    generic_device_action.contact = c1
    generic_device_action.device = d
    db.session.add_all([d, c1, u1, generic_device_action])
    db.session.commit()
    return generic_device_action


def generate_configuration_action_model(
    is_public=False, is_private=False, is_internal=True, cfg_permission_group=None
):
    """Generate a generic configuration action instance."""
    config = generate_configuration_model(
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
        cfg_permission_group=cfg_permission_group,
    )
    userinfo = generate_userinfo_data()
    c1 = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    u1 = User(subject=userinfo["sub"], contact=c1)

    generic_configuration_action = GenericConfigurationAction(
        description="test GenericConfigurationAction",
        action_type_name="testing",
        action_type_uri="testing.unittest.de",
        begin_date=utc_now(),
        end_date=None,
        created_by=u1,
    )
    generic_configuration_action.contact = c1
    generic_configuration_action.configuration = config
    db.session.add_all([config, c1, u1, generic_configuration_action])
    db.session.commit()
    return generic_configuration_action


class TestGenericActions(BaseTestCase):
    """Test for the generic action models."""

    def test_add_generic_platform_action_model(self):
        """Ensure Add generic platform action model."""
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
        """Ensure to add generic device action model."""
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
        """Ensure to add generic configuration action model."""
        configuration_action_model = generate_configuration_action_model()
        generic_configuration_action = (
            db.session.query(GenericConfigurationAction)
            .filter_by(action_type_name="testing")
            .one()
        )
        self.assertDictEqual(
            configuration_action_model.__dict__, generic_configuration_action.__dict__
        )
