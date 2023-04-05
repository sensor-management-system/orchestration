# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from project.api.models import (
    ConfigurationDynamicLocationBeginAction,
    Contact,
    Device,
    DeviceProperty,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data

from project.tests.models.test_configurations_model import generate_configuration_model


def add_dynamic_location_begin_action_model(
    is_public=False, is_private=False, is_internal=True
):
    device = Device(
        short_name="Device 555",
        is_public=is_public,
        is_private=is_private,
        is_internal=is_internal,
    )
    x_property = DeviceProperty(
        device=device,
        measuring_range_min=fake.pyfloat(),
        measuring_range_max=fake.pyfloat(),
        failure_value=fake.pyfloat(),
        accuracy=fake.pyfloat(),
        label=fake.pystr(),
        unit_uri=fake.uri(),
        unit_name=fake.pystr(),
        compartment_uri=fake.uri(),
        compartment_name=fake.pystr(),
        property_uri=fake.uri(),
        property_name="Test property_name",
        sampling_media_uri=fake.uri(),
        sampling_media_name=fake.pystr(),
    )
    config = generate_configuration_model(
        is_public=is_public, is_private=is_private, is_internal=is_internal
    )
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    configuration_dynamic_location_begin_action = (
        ConfigurationDynamicLocationBeginAction(
            begin_date="2021-08-21T10:00:50.542Z",
            end_date="2033-08-30T10:00:50.542Z",
            begin_description="test configuration_dynamic_location_begin_action",
            end_description="end",
            x_property=x_property,
            configuration=config,
            begin_contact=contact,
            end_contact=contact,
        )
    )
    db.session.add_all(
        [
            device,
            x_property,
            config,
            contact,
            configuration_dynamic_location_begin_action,
        ]
    )
    db.session.commit()
    return configuration_dynamic_location_begin_action


class TestConfigurationDynamicLocationActionModel(BaseTestCase):
    """Tests for the ConfigurationDynamicLocationBeginAction &
    ConfigurationDynamicLocationEndAction Models."""

    def test_add_configuration_dynamic_location_begin_action_model(self):
        """""Ensure Add configuration dynamic location begin action model."""

        configuration_dynamic_location_begin_action = (
            add_dynamic_location_begin_action_model()
        )
        self.assertTrue(configuration_dynamic_location_begin_action.id is not None)
        self.assertEqual(
            configuration_dynamic_location_begin_action.begin_description,
            "test configuration_dynamic_location_begin_action",
        )
