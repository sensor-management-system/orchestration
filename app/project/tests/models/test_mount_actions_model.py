from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.models.device import Device
from project.api.models.mount_actions import DeviceMountAction, PlatformMountAction
from project.api.models.platform import Platform
from project.api.models.user import User
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model


def add_mount_device_action_model():
    d = Device(
        short_name=fake.linux_processor(),
    )
    p_p = Platform(
        short_name="device parent platform",
    )
    jwt1 = generate_token_data()
    c1 = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )
    u1 = User(subject=jwt1["sub"], contact=c1)
    config = generate_configuration_model()
    mpa = DeviceMountAction(
        begin_date=fake.date(),
        description="test mount device action model",
        offset_x=fake.coordinate(),
        offset_y=fake.coordinate(),
        offset_z=fake.coordinate(),
        created_by=u1,
        device=d,
    )
    mpa.parent_platform = p_p
    mpa.configuration = config
    mpa.contact = c1
    db.session.add_all([d, p_p, c1, u1, config, mpa])
    db.session.commit()
    return mpa


class TestMountActionsModel(BaseTestCase):
    """
    Test mount actions models
    """

    def test_mount_platform_action_model(self):
        """""Ensure Add mount platform action model """
        p = Platform(
            short_name="short_name test",
        )
        p_p = Platform(
            short_name="parent platform",
        )
        jwt1 = generate_token_data()
        c1 = Contact(
            given_name=jwt1["given_name"],
            family_name=jwt1["family_name"],
            email=jwt1["email"],
        )
        u1 = User(subject=jwt1["sub"], contact=c1)
        config = generate_configuration_model()

        mpa = PlatformMountAction(
            begin_date=fake.date(),
            description="test mount platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            created_by=u1,
            platform=p,
        )

        mpa.parent_platform = p_p
        mpa.configuration = config
        mpa.contact = c1
        db.session.add_all([p, p_p, c1, u1, config, mpa])
        db.session.commit()
        mpa_r = (
            db.session.query(PlatformMountAction)
            .filter_by(description="test mount platform action model")
            .one()
        )
        self.assertEqual(
            mpa.parent_platform.short_name, mpa_r.parent_platform.short_name
        )
        self.assertDictEqual(mpa.__dict__, mpa_r.__dict__)

    def test_mount_device_action_model(self):
        """""Ensure Add mount device action model """
        mpa = add_mount_device_action_model()
        mpa_r = (
            db.session.query(DeviceMountAction)
            .filter_by(description="test mount device action model")
            .one()
        )
        self.assertEqual(
            mpa.parent_platform.short_name, mpa_r.parent_platform.short_name
        )
        self.assertDictEqual(mpa.__dict__, mpa_r.__dict__)
