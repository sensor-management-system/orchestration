# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the configuration model."""

from project.api.models import Contact
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def generate_configuration_model(
    is_public=False,
    is_private=False,
    is_internal=True,
    cfg_permission_group=None,
):
    """Generate some instances & return a configruation."""
    userinfo = generate_userinfo_data()
    device = Device(
        short_name=fake.linux_processor(),
        manufacturer_name=fake.company(),
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    device_parent_platform = Platform(
        short_name="device parent platform",
        manufacturer_name=fake.company(),
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    platform = Platform(
        short_name=fake.linux_processor(),
        manufacturer_name=fake.company(),
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    parent_platform = Platform(
        short_name="platform parent-platform",
        manufacturer_name=fake.company(),
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    configuration = Configuration(
        label="Config1",
        is_public=is_public,
        is_internal=is_internal,
        cfg_permission_group=cfg_permission_group,
    )
    db.session.add_all(
        [
            device,
            device_parent_platform,
            platform,
            parent_platform,
            contact,
            configuration,
        ]
    )
    db.session.commit()
    return configuration


class TestConfigurationsModel(BaseTestCase):
    """Tests for the Configurations Model."""

    def test_add_configuration_model(self):
        """Ensure to add a configuration model instance."""
        generate_configuration_model()

        c = db.session.query(Configuration).filter_by(label="Config1").first()
        self.assertEqual("Config1", c.label)
