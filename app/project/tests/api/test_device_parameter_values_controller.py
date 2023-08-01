# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the device parameter value controller."""
import datetime

import pytz

from project import base_url
from project.api.models import (
    Contact,
    Device,
    DeviceParameter,
    DeviceParameterValueChangeAction,
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


@fixtures.register("contact2", scope=lambda: db.session)
def create_contact2():
    """Create a second contact so that it can be used within the tests."""
    result = Contact(
        given_name="second", family_name="contact", email="second.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_contact", scope=lambda: db.session)
def create_super_contact():
    """Create a contact for the super user."""
    result = Contact(
        given_name="super", family_name="contact", email="super.contact@localhost"
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


@fixtures.register("user2", scope=lambda: db.session)
@fixtures.use(["contact2"])
def create_user2(contact2):
    """Create another normal user to use it in the tests."""
    result = User(contact=contact2, subject=contact2.email)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user", scope=lambda: db.session)
@fixtures.use(["super_contact"])
def create_super_user(super_contact):
    """Create a super user to use it in the tests."""
    result = User(contact=super_contact, subject=super_contact.email, is_superuser=True)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("private_device_of_user1", scope=lambda: db.session)
@fixtures.use(["user1"])
def create_private_device_of_user1(user1):
    """Create a private device."""
    result = Device(
        short_name="private device of user1",
        is_internal=False,
        is_public=False,
        is_private=True,
        created_by=user1,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("internal_device1", scope=lambda: db.session)
def create_internal_device1():
    """Create an internal device."""
    result = Device(
        short_name="internal device1",
        is_internal=True,
        is_public=False,
        is_private=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_device1", scope=lambda: db.session)
def create_public_device1():
    """Create a public device."""
    result = Device(
        short_name="public device1",
        is_internal=False,
        is_public=True,
        is_private=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_device2", scope=lambda: db.session)
def create_public_device2():
    """Create a second public device."""
    result = Device(
        short_name="public device2",
        is_internal=False,
        is_public=True,
        is_private=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestControllerDeviceParameterValues(BaseTestCase):
    """Tests for the controller to get the values for a device at a point in time."""

    def test_get_without_device_id(self):
        """Ensure we get an 404 for a non existing device."""
        url = f"{base_url}/controller/devices/9999/parameter-values"
        response = self.client.get(url)
        self.expect(response.status_code).to_equal(404)

    @fixtures.use(["internal_device1"])
    def test_internal_device_without_user(self, internal_device1):
        """Ensure we get an 401 if we don't have an user for an internal device."""
        url = f"{base_url}/controller/devices/{internal_device1.id}/parameter-values"
        response = self.client.get(url)
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["public_device1"])
    def test_public_device_no_parameters_no_timepoint(
        self,
        public_device1,
    ):
        """Ensure we get an 200 if we have a public device."""
        url = f"{base_url}/controller/devices/{public_device1.id}/parameter-values"
        response = self.client.get(url)
        self.expect(response.status_code).to_equal(400)

    @fixtures.use(["public_device1"])
    def test_public_device_no_parameters_no_valid_timepoint(
        self,
        public_device1,
    ):
        """Ensure we get an 200 if we have a public device."""
        url = f"{base_url}/controller/devices/{public_device1.id}/parameter-values"
        response = self.client.get(url, query_string={"timepoint": "abcdef"})
        self.expect(response.status_code).to_equal(400)

    @fixtures.use(["public_device1"])
    def test_public_device_no_parameters(
        self,
        public_device1,
    ):
        """Ensure we get an 200 if we have a public device."""
        url = f"{base_url}/controller/devices/{public_device1.id}/parameter-values"
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

    @fixtures.use(["internal_device1", "user1"])
    def test_internal_device_with_user(self, internal_device1, user1):
        """Ensure we get an 200 if we have an user for an internal device."""
        url = f"{base_url}/controller/devices/{internal_device1.id}/parameter-values"
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

    @fixtures.use(["private_device_of_user1", "user1"])
    def test_private_device_with_creator(self, private_device_of_user1, user1):
        """Ensure we get an 200 if we have the creator of the private device."""
        url = f"{base_url}/controller/devices/{private_device_of_user1.id}/parameter-values"
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

    @fixtures.use(["private_device_of_user1", "user2"])
    def test_private_device_with_other_user(self, private_device_of_user1, user2):
        """Ensure we get an 403 if we havn't the creator of the private device."""
        url = f"{base_url}/controller/devices/{private_device_of_user1.id}/parameter-values"
        with self.run_requests_as(user2):
            response = self.client.get(
                url,
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["private_device_of_user1", "super_user"])
    def test_private_device_with_super_user(self, private_device_of_user1, super_user):
        """Ensure we get an 200 if we have the super user."""
        url = f"{base_url}/controller/devices/{private_device_of_user1.id}/parameter-values"
        with self.run_requests_as(super_user):
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

    @fixtures.use(["public_device1", "public_device2"])
    def test_public_device_one_parameter(
        self,
        public_device1,
        public_device2,
    ):
        """Ensure we get an 200 if we have a public device."""
        parameter = DeviceParameter(
            device=public_device1,
            label="test value",
            description="some test description",
            unit_uri="https://cv/units/1",
            unit_name="n",
        )
        db.session.add(parameter)
        db.session.commit()

        url = f"{base_url}/controller/devices/{public_device1.id}/parameter-values"
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
                        "type": "device_parameter",
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
        # device
        url2 = f"{base_url}/controller/devices/{public_device2.id}/parameter-values"
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

    @fixtures.use(["public_device1", "contact1"])
    def test_public_device_one_parameter_two_changes(
        self,
        public_device1,
        contact1,
    ):
        """Ensure we extract the values for the timepoint."""
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
        db.session.add_all([parameter, change1, change2])
        db.session.commit()

        url = f"{base_url}/controller/devices/{public_device1.id}/parameter-values"
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

    def test_post(self):
        """Ensure that it is not allowed to post."""
        url = f"{base_url}/controller/devices/9999/parameter-values"
        response = self.client.post(
            url, data={}, content_type="application/vnd.api+json"
        )
        self.expect(response.status_code).to_equal(405)
