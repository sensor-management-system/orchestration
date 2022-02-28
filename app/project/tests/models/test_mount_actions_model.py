from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.models.device import Device
from project.api.models.mount_actions import DeviceMountAction, PlatformMountAction
from project.api.models.platform import Platform
from project.api.models.user import User
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.models.test_configurations_model import generate_configuration_model


def add_mount_device_action_model():
    d = Device(
        short_name=fake.linux_processor(),
        is_public=False,
        is_private=False,
        is_internal=True,
    )
    p_p = Platform(
        short_name="device parent platform",
        is_public=False,
        is_private=False,
        is_internal=True,
    )
    userinfo = generate_userinfo_data()
    c1 = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    u1 = User(subject=userinfo["sub"], contact=c1)
    config = generate_configuration_model()
    device_mount_action = DeviceMountAction(
        begin_date=fake.date(),
        description="test mount device action model",
        offset_x=fake.coordinate(),
        offset_y=fake.coordinate(),
        offset_z=fake.coordinate(),
        created_by=u1,
        device=d,
    )
    device_mount_action.parent_platform = p_p
    device_mount_action.configuration = config
    device_mount_action.contact = c1
    db.session.add_all([d, p_p, c1, u1, config, device_mount_action])
    db.session.commit()
    return device_mount_action


def add_mount_platform_action_model():
    p = Platform(
        short_name="short_name test",
        is_public=False,
        is_private=False,
        is_internal=True,
    )
    p_p = Platform(
        short_name="parent platform",
        is_public=False,
        is_private=False,
        is_internal=True,
    )
    userinfo = generate_userinfo_data()
    c1 = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    u1 = User(subject=userinfo["sub"], contact=c1)
    config = generate_configuration_model()
    platform_mount_action = PlatformMountAction(
        begin_date=fake.date(),
        description="test mount platform action model",
        offset_x=fake.coordinate(),
        offset_y=fake.coordinate(),
        offset_z=fake.coordinate(),
        created_by=u1,
        platform=p,
    )
    platform_mount_action.parent_platform = p_p
    platform_mount_action.configuration = config
    platform_mount_action.contact = c1
    db.session.add_all([p, p_p, c1, u1, config, platform_mount_action])
    db.session.commit()
    return platform_mount_action


class TestMountActionsModel(BaseTestCase):
    """
    Test mount actions models
    """

    def test_mount_platform_action_model(self):
        """""Ensure Add mount platform action model """
        platform_mount_action = add_mount_platform_action_model()
        mpa_r = (
            db.session.query(PlatformMountAction)
            .filter_by(description="test mount platform action model")
            .one()
        )
        self.assertEqual(
            platform_mount_action.parent_platform.short_name,
            mpa_r.parent_platform.short_name,
        )
        self.assertDictEqual(platform_mount_action.__dict__, mpa_r.__dict__)

    def test_mount_device_action_model(self):
        """""Ensure Add mount device action model """
        mount_device_action_model = add_mount_device_action_model()
        mount_device_action = (
            db.session.query(DeviceMountAction)
            .filter_by(description="test mount device action model")
            .one()
        )
        self.assertEqual(
            mount_device_action_model.parent_platform.short_name,
            mount_device_action.parent_platform.short_name,
        )
        self.assertDictEqual(
            mount_device_action_model.__dict__, mount_device_action.__dict__
        )
