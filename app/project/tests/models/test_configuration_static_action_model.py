from project.api.models import (
    ConfigurationStaticLocationBeginAction,
    Contact,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data

from project.tests.models.test_configurations_model import generate_configuration_model


def add_static_location_begin_action_model(
    is_public=False, is_private=False, is_internal=True
):
    config = generate_configuration_model(
        is_public=is_public, is_private=is_private, is_internal=is_internal
    )
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    configuration_static_location_begin_action = ConfigurationStaticLocationBeginAction(
        begin_date="2021-10-21T10:00:50.542Z",
        end_date="2033-10-22T10:00:50.542Z",
        begin_description="test configuration_static_location_begin_action",
        end_description="end",
        x=fake.coordinate(),
        y=fake.coordinate(),
        z=fake.coordinate(),
        epsg_code=None,
        elevation_datum_name=None,
        elevation_datum_uri=fake.uri(),
        configuration=config,
        begin_contact=contact,
        end_contact=contact,
    )
    db.session.add_all([config, contact, configuration_static_location_begin_action])
    db.session.commit()
    return configuration_static_location_begin_action


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
            configuration_static_location_begin_action.begin_description,
            "test configuration_static_location_begin_action",
        )
