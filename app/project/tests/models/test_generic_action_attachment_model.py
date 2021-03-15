from project.api.models import (
    ConfigurationAttachment,
    GenericConfigurationActionAttachment,
)
from project.api.models.base_model import db
from project.api.models.device_attachment import DeviceAttachment
from project.api.models.generic_action_attachments import (
    GenericDeviceActionAttachment,
    GenericPlatformActionAttachment,
)
from project.api.models.platform_attachment import PlatformAttachment
from project.tests.base import BaseTestCase, fake
from project.tests.models.test_generic_actions_models import (
    generate_configuration_action_model,
    generate_device_action_model,
    generate_platform_action_model,
)


def add_generic_configuration_action_attachment_model():
    configuration_action_model = generate_configuration_action_model()
    attachment1 = ConfigurationAttachment(
        label="configuration attachment1",
        url=fake.image_url(),
        configuration_id=configuration_action_model.configuration_id,
    )
    attachment2 = ConfigurationAttachment(
        label="configuration attachment2",
        url=fake.image_url(),
        configuration_id=configuration_action_model.configuration_id,
    )
    generic_configuration_action_attachment = GenericConfigurationActionAttachment()
    generic_configuration_action_attachment.action = configuration_action_model
    generic_configuration_action_attachment.attachment = attachment1
    generic_configuration_action_attachment.attachment = attachment2
    db.session.add_all(
        [attachment1, attachment2, generic_configuration_action_attachment]
    )
    db.session.commit()
    return configuration_action_model


def add_generic_device_action_attachment_model():
    device_action_model = generate_device_action_model()
    attachment1 = DeviceAttachment(
        label="device attachment1",
        url=fake.image_url(),
        device_id=device_action_model.device_id,
    )
    attachment2 = DeviceAttachment(
        label="device attachment2",
        url=fake.image_url(),
        device_id=device_action_model.device_id,
    )
    gpa_attachment = GenericDeviceActionAttachment()
    gpa_attachment.action = device_action_model
    gpa_attachment.attachment = attachment1
    gpa_attachment.attachment = attachment2
    db.session.add_all([attachment1, attachment2, gpa_attachment])
    db.session.commit()
    return device_action_model


def add_generic_platform_action_attachment_model():
    platform_action_model = generate_platform_action_model()
    attachment1 = PlatformAttachment(
        label="platform attachment1",
        url=fake.image_url(),
        platform_id=platform_action_model.platform_id,
    )
    attachment2 = PlatformAttachment(
        label="platform attachment2",
        url=fake.image_url(),
        platform_id=platform_action_model.platform_id,
    )
    generic_platform_action_attachment = GenericPlatformActionAttachment()
    generic_platform_action_attachment.action = platform_action_model
    generic_platform_action_attachment.attachment = attachment1
    generic_platform_action_attachment.attachment = attachment2
    db.session.add_all([attachment1, attachment2, generic_platform_action_attachment])
    db.session.commit()
    return platform_action_model


class TestGenericActionModel(BaseTestCase):
    """
    Test Generic Action Model
    """

    def test_add_generic_platform_action_attachment_model(self):
        """""Ensure Add generic platform action attachment model """
        generic_platform_action_attachment_model = (
            add_generic_platform_action_attachment_model()
        )
        generic_platform_action_attachment = (
            db.session.query(GenericPlatformActionAttachment)
            .filter_by(action_id=generic_platform_action_attachment_model.id)
            .one()
        )
        self.assertEqual(
            "test GenericPlatformAction",
            generic_platform_action_attachment.action.description,
        )

    def test_add_generic_device_action_attachment_model(self):
        """""Ensure Add generic device action attachment model """
        generic_device_action_attachment_model = (
            add_generic_device_action_attachment_model()
        )
        generic_device_action_attachment = (
            db.session.query(GenericDeviceActionAttachment)
            .filter_by(action_id=generic_device_action_attachment_model.id)
            .one()
        )
        self.assertEqual(
            "test GenericDeviceAction",
            generic_device_action_attachment.action.description,
        )

    def test_add_generic_configuration_action_attachment_model(self):
        """""Ensure Add generic configuration action attachment model """
        generic_device_action_attachment_model = (
            add_generic_configuration_action_attachment_model()
        )
        generic_device_action_attachment = (
            db.session.query(GenericConfigurationActionAttachment)
            .filter_by(action_id=generic_device_action_attachment_model.id)
            .one()
        )
        self.assertEqual(
            "test GenericConfigurationAction",
            generic_device_action_attachment.action.description,
        )
