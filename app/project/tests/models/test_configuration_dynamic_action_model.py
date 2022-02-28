from project.api.models import (
    ConfigurationDynamicLocationBeginAction,
    ConfigurationDynamicLocationEndAction,
    Contact,
    Device,
    DeviceProperty,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data

from project.tests.models.test_configurations_model import generate_configuration_model


def add_dynamic_location_begin_action_model():
    device = Device(short_name="Device 555")
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
    config = generate_configuration_model()
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    configuration_dynamic_location_begin_action = (
        ConfigurationDynamicLocationBeginAction(
            begin_date=fake.date(),
            description="test configuration_dynamic_location_begin_action",
            x_property=x_property,
            configuration=config,
            contact=contact,
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


def add_dynamic_location_end_action_model():
    config = generate_configuration_model()
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    configuration_dynamic_location_end_action = ConfigurationDynamicLocationEndAction(
        end_date=fake.date(),
        description="test configuration_dynamic_location_end_action",
        configuration=config,
        contact=contact,
    )
    db.session.add_all([config, contact, configuration_dynamic_location_end_action])
    db.session.commit()
    return configuration_dynamic_location_end_action


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
            configuration_dynamic_location_begin_action.description,
            "test configuration_dynamic_location_begin_action",
        )

    def test_add_configuration_dynamic_location_end_action_model(self):
        """""Ensure Add configuration dynamic location end action model."""
        configuration_dynamic_location_end_action = (
            add_dynamic_location_end_action_model()
        )
        self.assertTrue(configuration_dynamic_location_end_action.id is not None)
        self.assertEqual(
            configuration_dynamic_location_end_action.description,
            "test configuration_dynamic_location_end_action",
        )
