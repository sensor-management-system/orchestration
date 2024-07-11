# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the configuration parameter value controller."""
import datetime

import pytz

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationParameter,
    ConfigurationParameterValueChangeAction,
    Contact,
    Device,
    DeviceMountAction,
    DeviceParameter,
    DeviceParameterValueChangeAction,
    Platform,
    PlatformMountAction,
    PlatformParameter,
    PlatformParameterValueChangeAction,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, Fixtures

fixtures = Fixtures()


@fixtures.register("contact1", scope=lambda: db.session)
def create_contact1():
    """Create a single contact so that it can be used within the tests."""
    result = Contact(
        given_name="first", family_name="contact", email="first.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("internal_configuration1", scope=lambda: db.session)
def create_internal_configuration1():
    """Create an internal configuration."""
    result = Configuration(
        label="internal configuration1",
        is_internal=True,
        is_public=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_configuration1", scope=lambda: db.session)
def create_public_configuration1():
    """Create a public configuration."""
    result = Configuration(
        label="public configuration1",
        is_internal=False,
        is_public=True,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_configuration2", scope=lambda: db.session)
def create_public_configuration2():
    """Create a second public configuration."""
    result = Configuration(
        label="public configuration2",
        is_internal=False,
        is_public=True,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_device1", scope=lambda: db.session)
def create_public_device1():
    """Create a public device."""
    result = Device(
        short_name="public device1", is_public=True, is_internal=False, is_private=False
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_device2", scope=lambda: db.session)
def create_public_device2():
    """Create another public device."""
    result = Device(
        short_name="public device2", is_public=True, is_internal=False, is_private=False
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_platform1", scope=lambda: db.session)
def create_public_platform1():
    """Create a public platform."""
    result = Platform(
        short_name="public platform1",
        is_public=True,
        is_internal=False,
        is_private=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_platform2", scope=lambda: db.session)
def create_public_platform2():
    """Create another public platform."""
    result = Platform(
        short_name="public platform2",
        is_public=True,
        is_internal=False,
        is_private=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestControllerConfigurationParameterValues(BaseTestCase):
    """Tests for the controller to get the values for a configuration at a point in time."""

    def test_get_without_configuration_id(self):
        """Ensure we get an 404 for a non existing configuration."""
        url = f"{base_url}/controller/configurations/9999/parameter-values"
        response = self.client.get(url)
        self.expect(response.status_code).to_equal(404)

    @fixtures.use(["internal_configuration1"])
    def test_internal_configuration_without_user(self, internal_configuration1):
        """Ensure we get an 401 if we don't have an user for an internal config."""
        url = f"{base_url}/controller/configurations/{internal_configuration1.id}/parameter-values"
        response = self.client.get(url)
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["public_configuration1"])
    def test_public_configuration_no_parameters_no_timepoint(
        self,
        public_configuration1,
    ):
        """Ensure we get an 200 if we have a public config."""
        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        response = self.client.get(url)
        self.expect(response.status_code).to_equal(400)

    @fixtures.use(["public_configuration1"])
    def test_public_configuration_no_parameters_no_valid_timepoint(
        self,
        public_configuration1,
    ):
        """Ensure we get an 200 if we have a public config."""
        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        response = self.client.get(url, query_string={"timepoint": "abcdef"})
        self.expect(response.status_code).to_equal(400)

    @fixtures.use(["public_configuration1"])
    def test_public_configuration_no_parameters(
        self,
        public_configuration1,
    ):
        """Ensure we get an 200 if we have a public config."""
        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        response = self.client.get(
            url,
            query_string={
                "timepoint": datetime.datetime(
                    2023, 5, 3, 12, 47, 0, tzinfo=pytz.utc
                ).isoformat()
            },
        )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal({"jsonapi": {"version": "1.0"}, "data": []})

    @fixtures.use(["internal_configuration1", "user1"])
    def test_internal_configuration_with_user(self, internal_configuration1, user1):
        """Ensure we get an 200 if we have an user for an internal config."""
        url = f"{base_url}/controller/configurations/{internal_configuration1.id}/parameter-values"
        with self.run_requests_as(user1):
            response = self.client.get(
                url,
                query_string={
                    "timepoint": datetime.datetime(
                        2023, 5, 3, 12, 16, 0, tzinfo=pytz.utc
                    ).isoformat()
                },
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal({"jsonapi": {"version": "1.0"}, "data": []})

    @fixtures.use(["public_configuration1", "public_configuration2"])
    def test_public_configuration_one_parameter(
        self,
        public_configuration1,
        public_configuration2,
    ):
        """Ensure we get an 200 if we have a public config."""
        parameter = ConfigurationParameter(
            configuration=public_configuration1,
            label="test value",
            description="some test description",
            unit_uri="https://cv/units/1",
            unit_name="n",
        )
        db.session.add(parameter)
        db.session.commit()

        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        response = self.client.get(
            url,
            query_string={
                "timepoint": datetime.datetime(
                    2023, 5, 3, 12, 47, 0, tzinfo=pytz.utc
                ).isoformat()
            },
        )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal(
            {
                "jsonapi": {"version": "1.0"},
                "data": [
                    {
                        "id": str(parameter.id),
                        "type": "configuration_parameter",
                        "attributes": {
                            "label": parameter.label,
                            "value": None,
                            "unit_name": parameter.unit_name,
                            "unit_uri": parameter.unit_uri,
                        },
                    }
                ],
            }
        )

        # And we check that we don't get the parameter for another
        # configuration
        url2 = f"{base_url}/controller/configurations/{public_configuration2.id}/parameter-values"
        response2 = self.client.get(
            url2,
            query_string={
                "timepoint": datetime.datetime(
                    2023, 5, 3, 12, 47, 0, tzinfo=pytz.utc
                ).isoformat()
            },
        )
        self.expect(response2.status_code).to_equal(200)
        self.expect(response2.json).to_equal(
            {"jsonapi": {"version": "1.0"}, "data": []}
        )

    @fixtures.use(["public_configuration1", "contact1"])
    def test_public_configuration_one_parameter_two_changes(
        self,
        public_configuration1,
        contact1,
    ):
        """Ensure we extract the values for the timepoint."""
        parameter = ConfigurationParameter(
            configuration=public_configuration1,
            label="test value",
            description="some test description",
            unit_uri="https://cv/units/1",
            unit_name="n",
        )
        change1 = ConfigurationParameterValueChangeAction(
            configuration_parameter=parameter,
            value="123",
            date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            contact=contact1,
            description="",
        )
        change2 = ConfigurationParameterValueChangeAction(
            configuration_parameter=parameter,
            value="456",
            date=datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            contact=contact1,
            description="",
        )
        db.session.add_all([parameter, change1, change2])
        db.session.commit()

        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        expected_results = {
            datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc): None,
            datetime.datetime(2022, 2, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "123",
            datetime.datetime(2023, 2, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "456",
            datetime.datetime(2023, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "456",
            datetime.datetime(2022, 12, 31, 23, 59, 59, 999, tzinfo=pytz.utc): "123",
        }
        for timepoint, expected_result in expected_results.items():
            response = self.client.get(
                url,
                query_string={
                    "timepoint": timepoint.isoformat(),
                },
            )
            self.expect(response.status_code).to_equal(200)
            self.expect(response.json).to_equal(
                {
                    "jsonapi": {"version": "1.0"},
                    "data": [
                        {
                            "id": str(parameter.id),
                            "type": "configuration_parameter",
                            "attributes": {
                                "label": parameter.label,
                                "value": expected_result,
                                "unit_name": parameter.unit_name,
                                "unit_uri": parameter.unit_uri,
                            },
                        }
                    ],
                }
            )

    def test_post(self):
        """Ensure that it is not allowed to post."""
        url = f"{base_url}/controller/configurations/9999/parameter-values"
        response = self.client.post(
            url, data={}, content_type="application/vnd.api+json"
        )
        self.expect(response.status_code).to_equal(405)

    @fixtures.use(["public_configuration1"])
    def test_public_configuration_without_mounts(
        self,
        public_configuration1,
    ):
        """Ensure we extract the values for the timepoint without any mounts."""
        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        timepoint = datetime.datetime(2023, 5, 3, 15, 12, 0, 0, tzinfo=pytz.utc)
        response = self.client.get(
            url,
            query_string={
                "timepoint": timepoint.isoformat(),
            },
        )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal({"jsonapi": {"version": "1.0"}, "data": []})

    @fixtures.use(["public_configuration1", "public_device1", "contact1"])
    def test_public_configuration_with_device_mount(
        self,
        public_configuration1,
        public_device1,
        contact1,
    ):
        """Ensure we extract the values for the timepoint from a device mount."""
        mount = DeviceMountAction(
            device=public_device1,
            configuration=public_configuration1,
            begin_date=datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            begin_contact=contact1,
            end_date=datetime.datetime(2038, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            end_contact=contact1,
        )
        parameter = DeviceParameter(
            device=public_device1,
            label="test value",
            description="some test description",
            unit_uri="https://cv/units/1",
            unit_name="n",
        )
        change1 = DeviceParameterValueChangeAction(
            device_parameter=parameter,
            value="123",
            date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            contact=contact1,
            description="",
        )
        change2 = DeviceParameterValueChangeAction(
            device_parameter=parameter,
            value="456",
            date=datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            contact=contact1,
            description="",
        )
        db.session.add_all([mount, parameter, change1, change2])
        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        expected_results = {
            datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc): None,
            datetime.datetime(2022, 2, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "123",
            datetime.datetime(2023, 2, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "456",
            datetime.datetime(2023, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "456",
            datetime.datetime(2022, 12, 31, 23, 59, 59, 999, tzinfo=pytz.utc): "123",
        }
        for timepoint, expected_result in expected_results.items():
            response = self.client.get(
                url,
                query_string={
                    "timepoint": timepoint.isoformat(),
                },
            )
            self.expect(response.status_code).to_equal(200)
            self.expect(response.json).to_equal(
                {
                    "jsonapi": {"version": "1.0"},
                    "data": [
                        {
                            "id": str(parameter.id),
                            "type": "device_parameter",
                            "attributes": {
                                "label": parameter.label,
                                "value": expected_result,
                                "unit_name": parameter.unit_name,
                                "unit_uri": parameter.unit_uri,
                            },
                        }
                    ],
                }
            )

        # And completely before the device was mounted.
        response = self.client.get(
            url,
            query_string={
                "timepoint": datetime.datetime(1990, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            },
        )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal({"jsonapi": {"version": "1.0"}, "data": []})
        # And completely after the device was unmounted.
        response = self.client.get(
            url,
            query_string={
                "timepoint": datetime.datetime(2090, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            },
        )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal({"jsonapi": {"version": "1.0"}, "data": []})

    @fixtures.use(["public_configuration1", "public_platform1", "contact1"])
    def test_public_configuration_with_platform_mount(
        self,
        public_configuration1,
        public_platform1,
        contact1,
    ):
        """Ensure we extract the values for the timepoint from a platform mount."""
        mount = PlatformMountAction(
            platform=public_platform1,
            configuration=public_configuration1,
            begin_date=datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            begin_contact=contact1,
            end_date=datetime.datetime(2038, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            end_contact=contact1,
        )
        parameter = PlatformParameter(
            platform=public_platform1,
            label="test value",
            description="some test description",
            unit_uri="https://cv/units/1",
            unit_name="n",
        )
        change1 = PlatformParameterValueChangeAction(
            platform_parameter=parameter,
            value="123",
            date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            contact=contact1,
            description="",
        )
        change2 = PlatformParameterValueChangeAction(
            platform_parameter=parameter,
            value="456",
            date=datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            contact=contact1,
            description="",
        )
        db.session.add_all([mount, parameter, change1, change2])
        url = f"{base_url}/controller/configurations/{public_configuration1.id}/parameter-values"
        expected_results = {
            datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc): None,
            datetime.datetime(2022, 2, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "123",
            datetime.datetime(2023, 2, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "456",
            datetime.datetime(2023, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc): "456",
            datetime.datetime(2022, 12, 31, 23, 59, 59, 999, tzinfo=pytz.utc): "123",
        }
        for timepoint, expected_result in expected_results.items():
            response = self.client.get(
                url,
                query_string={
                    "timepoint": timepoint.isoformat(),
                },
            )
            self.expect(response.status_code).to_equal(200)
            self.expect(response.json).to_equal(
                {
                    "jsonapi": {"version": "1.0"},
                    "data": [
                        {
                            "id": str(parameter.id),
                            "type": "platform_parameter",
                            "attributes": {
                                "label": parameter.label,
                                "value": expected_result,
                                "unit_name": parameter.unit_name,
                                "unit_uri": parameter.unit_uri,
                            },
                        }
                    ],
                }
            )

        # And completely before the platform was mounted.
        response = self.client.get(
            url,
            query_string={
                "timepoint": datetime.datetime(1990, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            },
        )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal({"jsonapi": {"version": "1.0"}, "data": []})
        # And completely after the platform was unmounted.
        response = self.client.get(
            url,
            query_string={
                "timepoint": datetime.datetime(2090, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            },
        )
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json).to_equal({"jsonapi": {"version": "1.0"}, "data": []})
