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
        is_public=True,
        is_private=False,
        is_internal=False,
    )
    mock_jwt = generate_token_data()
    c1 = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    u1 = User(subject=mock_jwt["sub"], contact=c1)
    config = generate_configuration_model()
    unmount_device_action = DeviceUnmountAction(
        end_date=fake.date(),
        description="test unmount device action model",
        created_by=u1,
        device=d,
    )
    unmount_device_action.configuration = config
    unmount_device_action.contact = c1
    db.session.add_all([d, c1, u1, config, unmount_device_action])
    db.session.commit()
    return unmount_device_action


def add_unmount_platform_action():
    p = Platform(
        short_name="Platform 55", is_public=True, is_private=False, is_internal=False,
    )
    mock_jwt = generate_token_data()
    c1 = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    u1 = User(subject=mock_jwt["sub"], contact=c1)
    config = generate_configuration_model()
    unmount_platform_action = PlatformUnmountAction(
        end_date=fake.date(),
        description="test unmount platform action model",
        created_by=u1,
        platform=p,
    )
    unmount_platform_action.configuration = config
    unmount_platform_action.contact = c1
    db.session.add_all([p, c1, u1, config, unmount_platform_action])
    db.session.commit()
    return unmount_platform_action


class TestUnMountActionModel(BaseTestCase):
    """
    Test unmount action Models
    """

    def test_unmount_platform_action_model(self):
        """""Ensure Add unmount platform action model """
        unmount_platform_action_model = add_unmount_platform_action()
        unmount_platform_action = (
            db.session.query(PlatformUnmountAction)
            .filter_by(description="test unmount platform action model")
            .one()
        )
        self.assertEqual(
            unmount_platform_action_model.description,
            unmount_platform_action.description,
        )
        self.assertDictEqual(
            unmount_platform_action_model.__dict__, unmount_platform_action.__dict__
        )

    def test_unmount_device_action_model(self):
        """""Ensure Add unmount device action model """
        unmount_device_action_model = add_unmount_device_action()
        unmount_device_action = (
            db.session.query(DeviceUnmountAction)
            .filter_by(description="test unmount device action model")
            .one()
        )
        self.assertEqual(
            unmount_device_action_model.description, unmount_device_action.description
        )
        self.assertDictEqual(
            unmount_device_action_model.__dict__, unmount_device_action.__dict__
        )
