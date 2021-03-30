from project.api.models import (
    ConfigurationStaticLocationBeginAction,
    ConfigurationStaticLocationEndAction,
    Contact,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_token_data

from .test_configurations_model import generate_configuration_model


def add_static_location_begin_action_model():
    config = generate_configuration_model()
    mock_jwt = generate_token_data()
    contact = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    configuration_static_location_begin_action = ConfigurationStaticLocationBeginAction(
        begin_date=fake.date(),
        description="test configuration_static_location_begin_action",
        x=fake.coordinate(),
        y=fake.coordinate(),
        z=fake.coordinate(),
        epsg_code=None,
        elevation_datum_name=None,
        elevation_datum_uri=fake.uri(),
        configuration=config,
        contact=contact,
    )
    db.session.add_all([config, contact, configuration_static_location_begin_action])
    db.session.commit()
    return configuration_static_location_begin_action


def add_static_location_end_action_model():
    config = generate_configuration_model()
    mock_jwt = generate_token_data()
    contact = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    configuration_static_location_end_action = ConfigurationStaticLocationEndAction(
        end_date=fake.date(),
        description="test configuration_static_location_end_action",
        configuration=config,
        contact=contact,
    )
    db.session.add_all([config, contact, configuration_static_location_end_action])
    db.session.commit()
    return configuration_static_location_end_action


class TestConfigurationStaticLocationActionModel(BaseTestCase):
    """Tests for the ConfigurationStaticLocationBeginAction &
    ConfigurationStaticLocationEndAction Models."""

    def test_add_configuration_static_location_begin_action_model(self):
        """""Ensure Add configuration static location begin action model."""

        configuration_static_location_begin_action = (
            add_static_location_begin_action_model()
        )
        self.assertTrue(configuration_static_location_begin_action.id is not None)
        self.assertEqual(
            configuration_static_location_begin_action.description,
            "test configuration_static_location_begin_action",
        )

    def test_add_configuration_static_location_end_action_model(self):
        """""Ensure Add configuration static location end action model."""
        configuration_static_location_end_action = (
            add_static_location_end_action_model()
        )
        self.assertTrue(configuration_static_location_end_action.id is not None)
        self.assertEqual(
            configuration_static_location_end_action.description,
            "test configuration_static_location_end_action",
        )
