"""Tests for the location actions controller."""

import datetime

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationStaticLocationBeginAction,
    ConfigurationDynamicLocationBeginAction,
    Contact,
    User
)
from project.tests.models.test_configuration_static_action_model import (
    add_static_location_begin_action_model,
)
from project.api.models.base_model import db
from project.api.schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationBeginActionSchema
)
from project.api.schemas.configuration_dynamic_location_actions_schema import ConfigurationDynamicLocationBeginActionSchema

from project.tests.base import BaseTestCase


class TestControllerConfigurationsLocationActions(BaseTestCase):

    def setUp(self):
        """Set up some example data that will be used in most of  the tests."""
        super().setUp()

        contact = Contact(given_name="D", family_name="U", email="d.u@localhost")
        self.configuration = Configuration(
            label="dummy configuration", is_internal=True
        )
        self.u = User(subject="du", contact=contact)
        db.session.add_all(
            [contact, self.u, self.configuration]

        )
        db.session.commit()
        self.url = (
                f"{base_url}/controller/configurations/"
                + f"{self.configuration.id}/location-action-timepoints"
        )

    def test_get_without_configuration_id(self):
        """Ensure that we get a 404 for a non existing configuration."""
        url = (
            f"{base_url}/controller/configurations/9999/location-action-timepoints"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_empty(self):
        """Ensure we get an empty list if there is no action."""
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_internal_without_user(self):
        """Ensure anonymous can't access an internal configuration."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_one_location_action_static(self):
        """Ensure we get an entry for an existing location action."""

        configuration_static_location_begin_action = ConfigurationStaticLocationBeginAction(
            begin_date=datetime.datetime(2021, 10, 31, 10, 0, 0),
            begin_description="test configuration_static_location_begin_action",
            x=20.0,
            y=20.0,
            z=20.0,
            epsg_code=None,
            elevation_datum_name=None,
            elevation_datum_uri="http://wilkerson-harris.com/",
            configuration=self.configuration,
            begin_contact=self.u.contact,
        )
        db.session.add(configuration_static_location_begin_action)
        db.session.commit()

        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2021-10-31T10:00:00",
                "type": "configuration_static_location_begin",
                "attributes": ConfigurationStaticLocationBeginActionSchema().dump(
                    configuration_static_location_begin_action)["data"]["attributes"],
            }]

        self.assertEqual(response.json, expected)

    def test_get_one_location_action_dynamic(self):
        """Ensure we get an entry for an existing dynamic location action."""

        configuration_dynamic_location_begin_action = ConfigurationDynamicLocationBeginAction(
            begin_date=datetime.datetime(2021, 10, 31, 10, 0, 0),
            begin_description="test configuration_location_begin_action",
            configuration=self.configuration,
            begin_contact=self.u.contact,
        )
        db.session.add(configuration_dynamic_location_begin_action)
        db.session.commit()

        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2021-10-31T10:00:00",
                "type": "configuration_dynamic_location_begin",
                "attributes": ConfigurationDynamicLocationBeginActionSchema().dump(
                    configuration_dynamic_location_begin_action)["data"]["attributes"],
            }]

        self.assertEqual(response.json, expected)

    def test_response_is_ordered_by_begin_date(self):
        """Ensure that a list of location actions is ordered by begin date."""
        configuration_static_location_begin_action = ConfigurationStaticLocationBeginAction(
            begin_date=datetime.datetime(2021, 10, 31, 10, 0, 0),
            end_date=datetime.datetime(2021, 11, 1, 12, 0, 0),
            begin_description="test configuration_static_location_begin_action",
            end_description="end",
            x=20.0,
            y=20.0,
            z=20.0,
            epsg_code=None,
            elevation_datum_name=None,
            elevation_datum_uri="http://wilkerson-harris.com/",
            configuration=self.configuration,
            begin_contact=self.u.contact,
            end_contact=self.u.contact,
        )
        configuration_static_location_begin_action1 = ConfigurationStaticLocationBeginAction(
            begin_date=datetime.datetime(2011, 11, 25, 10, 0, 0),
            end_date=datetime.datetime(2011, 11, 26, 12, 0, 0),
            begin_description="test configuration_static_location_begin_action",
            end_description="end",
            x=21.0,
            y=21.0,
            z=21.0,
            epsg_code=None,
            elevation_datum_name=None,
            elevation_datum_uri="http://luna.com/",
            configuration=self.configuration,
            begin_contact=self.u.contact,
            end_contact=self.u.contact,
        )
        configuration_dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            begin_date=datetime.datetime(2024, 1, 13, 22, 56, 57),
            end_date=datetime.datetime(2025, 12, 25, 1, 1, 2),
            begin_description="Test dynamic locatiion begin",
            end_description="Test dynamic location end",
            configuration=self.configuration,
            begin_contact=self.u.contact,
            end_contact=self.u.contact
        )
        db.session.add_all([configuration_static_location_begin_action, configuration_static_location_begin_action1, configuration_dynamic_location_action])
        db.session.commit()

        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2011-11-25T10:00:00",
                "type": "configuration_static_location_begin",
                "attributes": ConfigurationStaticLocationBeginActionSchema().dump(
                    configuration_static_location_begin_action1)["data"]["attributes"],
            },
            {
                "timepoint": "2021-10-31T10:00:00",
                "type": "configuration_static_location_begin",
                "attributes": ConfigurationStaticLocationBeginActionSchema().dump(
                    configuration_static_location_begin_action)["data"]["attributes"],
            },
            {
                "timepoint": "2024-01-13T22:56:57",
                "type": "configuration_dynamic_location_begin",
                "attributes": ConfigurationDynamicLocationBeginActionSchema().dump(configuration_dynamic_location_action)["data"]["attributes"]
            },
        ]
        self.assertEqual(response.json, expected)

    def test_response_with_end_dates(self):
        """Ensure that a list of location actions can include end dates."""
        configuration_static_location_begin_action = ConfigurationStaticLocationBeginAction(
            begin_date=datetime.datetime(2021, 10, 31, 10, 0, 0),
            end_date=datetime.datetime(2021, 11, 1, 12, 0, 0),
            begin_description="test configuration_static_location_begin_action",
            end_description="end",
            x=20.0,
            y=20.0,
            z=20.0,
            epsg_code=None,
            elevation_datum_name=None,
            elevation_datum_uri="http://wilkerson-harris.com/",
            configuration=self.configuration,
            begin_contact=self.u.contact,
            end_contact=self.u.contact,
        )
        configuration_static_location_begin_action1 = ConfigurationStaticLocationBeginAction(
            begin_date=datetime.datetime(2011, 11, 25, 10, 0, 0),
            end_date=datetime.datetime(2011, 11, 26, 12, 0, 0),
            begin_description="test configuration_static_location_begin_action",
            end_description="end",
            x=21.0,
            y=21.0,
            z=21.0,
            epsg_code=None,
            elevation_datum_name=None,
            elevation_datum_uri="http://luna.com/",
            configuration=self.configuration,
            begin_contact=self.u.contact,
            end_contact=self.u.contact,
        )
        configuration_dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            begin_date=datetime.datetime(2024, 1, 13, 22, 56, 57),
            end_date=datetime.datetime(2025, 12, 25, 1, 1, 2),
            begin_description="Test dynamic locatiion begin",
            end_description="Test dynamic location end",
            configuration=self.configuration,
            begin_contact=self.u.contact,
            end_contact=self.u.contact
        )
        db.session.add_all([configuration_static_location_begin_action, configuration_static_location_begin_action1, configuration_dynamic_location_action])
        db.session.commit()

        with self.run_requests_as(self.u):
            response = self.client.get(self.url + '?include_ends=true')
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2011-11-25T10:00:00",
                "type": "configuration_static_location_begin",
                "attributes": ConfigurationStaticLocationBeginActionSchema().dump(
                    configuration_static_location_begin_action1)["data"]["attributes"],
            },
            {
                "timepoint": "2011-11-26T12:00:00",
                "type": "configuration_static_location_end",
                "attributes": ConfigurationStaticLocationBeginActionSchema().dump(
                    configuration_static_location_begin_action1)["data"]["attributes"],
            },
            {
                "timepoint": "2021-10-31T10:00:00",
                "type": "configuration_static_location_begin",
                "attributes": ConfigurationStaticLocationBeginActionSchema().dump(
                    configuration_static_location_begin_action)["data"]["attributes"],
            },
            {
                "timepoint": "2021-11-01T12:00:00",
                "type": "configuration_static_location_end",
                "attributes": ConfigurationStaticLocationBeginActionSchema().dump(
                    configuration_static_location_begin_action)["data"]["attributes"],
            },
            {
                "timepoint": "2024-01-13T22:56:57",
                "type": "configuration_dynamic_location_begin",
                "attributes": ConfigurationDynamicLocationBeginActionSchema().dump(configuration_dynamic_location_action)["data"]["attributes"]
            },
            {
                "timepoint": "2025-12-25T01:01:02",
                "type": "configuration_dynamic_location_end",
                "attributes": ConfigurationDynamicLocationBeginActionSchema().dump(configuration_dynamic_location_action)["data"]["attributes"]
            }
        ]
        self.assertEqual(response.json, expected)
