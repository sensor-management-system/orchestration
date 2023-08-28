# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the generic action attachment models."""
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


def add_generic_configuration_action_model():
    """Create a generic configuration action model with attachments."""
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


def add_generic_device_action_model():
    """Create a generic device action model with attachments."""
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


def add_generic_platform_action_model():
    """Create a generic platform action model with attachments."""
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
    """Tess for the generic action attachment models."""

    def test_add_generic_platform_action_attachment_model(self):
        """Ensure Add generic platform action attachment model."""
        generic_platform_action_model = add_generic_platform_action_model()
        generic_platform_action_attachment = (
            db.session.query(GenericPlatformActionAttachment)
            .filter_by(action_id=generic_platform_action_model.id)
            .one()
        )
        self.assertEqual(
            "test GenericPlatformAction",
            generic_platform_action_attachment.action.description,
        )

    def test_add_generic_device_action_attachment_model(self):
        """Ensure Add generic device action attachment model."""
        generic_device_action_model = add_generic_device_action_model()
        generic_device_action_attachment = (
            db.session.query(GenericDeviceActionAttachment)
            .filter_by(action_id=generic_device_action_model.id)
            .one()
        )
        self.assertEqual(
            "test GenericDeviceAction",
            generic_device_action_attachment.action.description,
        )

    def test_add_generic_configuration_action_attachment_model(self):
        """Ensure Add generic configuration action attachment model."""
        generic_device_action_model = add_generic_configuration_action_model()
        generic_device_action_attachment = (
            db.session.query(GenericConfigurationActionAttachment)
            .filter_by(action_id=generic_device_action_model.id)
            .one()
        )
        self.assertEqual(
            "test GenericConfigurationAction",
            generic_device_action_attachment.action.description,
        )
