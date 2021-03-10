from project.api.models import (
    Contact,
    Device,
    DeviceUnmountAction,
    Platform,
    PlatformUnmountAction,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model


def add_unmount_device_action():
    d = Device(
        short_name=fake.linux_processor(),
    )
    jwt1 = generate_token_data()
    c1 = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )
    u1 = User(subject=jwt1["sub"], contact=c1)
    config = generate_configuration_model()
    mpa = DeviceUnmountAction(
        end_date=fake.date(),
        description="test unmount device action model",
        created_by=u1,
        device=d,
    )
    mpa.configuration = config
    mpa.contact = c1
    db.session.add_all([d, c1, u1, config, mpa])
    db.session.commit()
    return mpa


def add_unmount_platform_action():
    p = Platform(
        short_name="Platform 2322",
    )
    jwt1 = generate_token_data()
    c1 = Contact(
        given_name=jwt1["given_name"],
        family_name=jwt1["family_name"],
        email=jwt1["email"],
    )
    u1 = User(subject=jwt1["sub"], contact=c1)
    config = generate_configuration_model()
    mpa = PlatformUnmountAction(
        end_date=fake.date(),
        description="test unmount platform action model",
        created_by=u1,
        platform=p,
    )
    mpa.configuration = config
    mpa.contact = c1
    db.session.add_all([p, c1, u1, config, mpa])
    db.session.commit()
    return mpa


class TestUnMountActionModel(BaseTestCase):
    """
    Test unmount action Models
    """

    def test_unmount_platform_action_model(self):
        """""Ensure Add unmount platform action model """
        mpa = add_unmount_platform_action()
        mpa_r = (
            db.session.query(PlatformUnmountAction)
            .filter_by(description="test unmount platform action model")
            .one()
        )
        self.assertEqual(
            mpa.parent_platform.short_name, mpa_r.parent_platform.short_name
        )
        self.assertDictEqual(mpa.__dict__, mpa_r.__dict__)

    def test_unmount_device_action_model(self):
        """""Ensure Add unmount device action model """
        mpa = add_unmount_device_action()
        mpa_r = (
            db.session.query(DeviceUnmountAction)
            .filter_by(description="test unmount device action model")
            .one()
        )
        self.assertEqual(
            mpa.parent_platform.short_name, mpa_r.parent_platform.short_name
        )
        self.assertDictEqual(mpa.__dict__, mpa_r.__dict__)
