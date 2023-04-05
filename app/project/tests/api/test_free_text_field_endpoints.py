# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Luca Johannes Nendel <Luca-Johannes.Nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Classes to test the endpoints to reflect free text fields."""

from datetime import datetime

from flask import url_for

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationCustomField,
    Contact,
    CustomField,
    Device,
    DeviceCalibrationAction,
    DeviceProperty,
    DeviceSoftwareUpdateAction,
    GenericConfigurationAction,
    GenericDeviceAction,
    GenericPlatformAction,
    Platform,
    PlatformSoftwareUpdateAction,
    Site,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestDeviceShortNameEndpoint(BaseTestCase):
    """Tests for the short name endpoint for devices."""

    url = f"{base_url}/controller/device-short-names"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_device(self):
        """Ensure we can get a response for one device with one entry."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_get_for_two_devices(self):
        """Ensure we can get a response for two device with two entries."""
        device1 = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="short dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "short dummy"])

    def test_get_for_two_devices_with_same_short_name(self):
        """Ensure we can get a response for two device with one short name."""
        device1 = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_get_for_one_device_and_one_platform(self):
        """
        Ensure we can get a response for only the one device.

        There should be no ínteraction with platforms.
        """
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_short_name_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_short_name_of_private_device_is_included_for_owner(self):
        """Ensure we give out private device data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])


class TestDeviceLongNameEndpoint(BaseTestCase):
    """Tests for the long name endpoint for devices."""

    url = f"{base_url}/controller/device-long-names"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_device(self):
        """Ensure we can get a response for one device with one entry."""
        device = Device(
            short_name="dummy",
            long_name="long dummy name",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add(device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["long dummy name"])

    def test_get_for_one_device_without_longname(self):
        """Ensure we can get a response for one device with one entry."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_device_with_null_as_longname(self):
        """Ensure we can get a response for one device with one entry."""
        device = Device(
            short_name="dummy",
            long_name=None,
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add(device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_device_with_empty_as_longname(self):
        """Ensure we can get a response for one device with one entry."""
        device = Device(
            short_name="dummy",
            long_name="",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add(device)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_two_devices(self):
        """Ensure we can get a response for two device with two entries."""
        device1 = Device(
            short_name="dummy",
            long_name="long dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="short dummy",
            long_name="very long dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["long dummy", "very long dummy"])

    def test_get_for_two_devices_with_same_long_name(self):
        """Ensure we can get a response for two device with one long name."""
        device1 = Device(
            short_name="dummy 2",
            long_name="longer name",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="dummy 3",
            long_name="longer name",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["longer name"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_long_name_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1",
            long_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            long_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_long_name_of_private_device_is_included_for_owner(self):
        """Ensure we give out private device data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1",
            long_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            long_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])


class TestPlatformShortNameEndpoint(BaseTestCase):
    """Tests for the short name endpoint for platforms."""

    url = f"{base_url}/controller/platform-short-names"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_platform(self):
        """Ensure we can get a response for one platform with one entry."""
        platform = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_get_for_two_platforms(self):
        """Ensure we can get a response for two platform with two entries."""
        platform1 = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="short dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "short dummy"])

    def test_get_for_two_platforms_with_same_short_name(self):
        """Ensure we can get a response for two platform with one short name."""
        platform1 = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_get_for_one_platform_and_one_platform(self):
        """
        Ensure we can get a response for only the one platform.

        There should be no ínteraction with platforms.
        """
        platform = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_short_name_of_private_platform_is_not_included_for_other(self):
        """Ensure we don't show data for private platforms to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_short_name_of_private_platform_is_included_for_owner(self):
        """Ensure we give out private platform data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])


class TestPlatformLongNameEndpoint(BaseTestCase):
    """Tests for the long name endpoint for platforms."""

    url = f"{base_url}/controller/platform-long-names"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_platform(self):
        """Ensure we can get a response for one platform with one entry."""
        platform = Platform(
            short_name="dummy",
            long_name="long dummy name",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add(platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["long dummy name"])

    def test_get_for_one_platform_without_longname(self):
        """Ensure we can get a response for one platform with one entry."""
        platform = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        db.session.add(platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_platform_with_null_as_longname(self):
        """Ensure we can get a response for one platform with one entry."""
        platform = Platform(
            short_name="dummy",
            long_name=None,
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add(platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_one_platform_with_empty_as_longname(self):
        """Ensure we can get a response for one platform with one entry."""
        platform = Platform(
            short_name="dummy",
            long_name="",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add(platform)
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_two_platforms(self):
        """Ensure we can get a response for two platform with two entries."""
        platform1 = Platform(
            short_name="dummy",
            long_name="long dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="short dummy",
            long_name="very long dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["long dummy", "very long dummy"])

    def test_get_for_two_platforms_with_same_long_name(self):
        """Ensure we can get a response for two platform with one long name."""
        platform1 = Platform(
            short_name="dummy 2",
            long_name="longer name",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="dummy 3",
            long_name="longer name",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["longer name"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_long_name_of_private_platform_is_not_included_for_other(self):
        """Ensure we don't show data for private platforms to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="d1",
            long_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            long_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_long_name_of_private_platform_is_included_for_owner(self):
        """Ensure we give out private platform data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="d1",
            long_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            long_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])


class TestDeviceManufacturerNames(BaseTestCase):
    """Tests for the endpoints for the device manufacturer names."""

    url = f"{base_url}/controller/device-manufacturer-names"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_manufacturers(self):
        """Ensure we get a list of manufacturer names."""
        device1 = Device(
            short_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
            manufacturer_name="Device GmbH",
        )
        device2 = Device(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            manufacturer_name="Device GmbH",
        )
        device3 = Device(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            manufacturer_name="Alternative & Co",
        )

        db.session.add_all([device1, device2, device3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["Alternative & Co", "Device GmbH"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_manufacturer_name_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1",
            manufacturer_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            manufacturer_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_manufacturer_name_of_private_device_is_included_for_owner(self):
        """Ensure we give out private device data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1",
            manufacturer_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            manufacturer_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])


class TestDeviceSerialNumbers(BaseTestCase):
    """Tests for the endpoints for the device serial numbers."""

    url = f"{base_url}/controller/device-serial-numbers"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_serial_numbers(self):
        """Ensure we get a list of serial numbers."""
        device1 = Device(
            short_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
            serial_number="69",
        )
        device2 = Device(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            serial_number="69",
        )
        device3 = Device(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            serial_number="23",
        )

        db.session.add_all([device1, device2, device3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["23", "69"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_serial_number_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            serial_number="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_serial_number_of_private_device_is_included_for_owner(self):
        """Ensure we give out private device data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            serial_number="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])

    def test_ignore_by_ids(self):
        """Ensure we can ignore the entries that come from certain ids."""
        device1 = Device(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            serial_number="fancy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url + f"?ignore={device1.id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["fancy"])

    def test_prefilter_by_short_name(self):
        """Ensure we can filter the set by a given short name."""
        device1 = Device(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            serial_number="fancy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url + f"?short_name={device1.short_name}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_prefilter_by_manufacturer_name(self):
        """Ensure we can filter the set by a manufacturer name."""
        device1 = Device(
            short_name="d1",
            serial_number="dummy",
            manufacturer_name="m1",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            serial_number="fancy",
            manufacturer_name="m2",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(
                self.url + f"?manufacturer_name={device1.manufacturer_name}"
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_prefilter_by_manufacturer_uri(self):
        """Ensure we can filter the set by a manufacturer name."""
        device1 = Device(
            short_name="d1",
            serial_number="dummy",
            manufacturer_uri="m1",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            serial_number="fancy",
            manufacturer_uri="m2",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(
                self.url + f"?manufacturer_uri={device1.manufacturer_uri}"
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_prefilter_by_model(self):
        """Ensure we can filter the set by a manufacturer name."""
        device1 = Device(
            short_name="d1",
            serial_number="dummy",
            model="m1",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        device2 = Device(
            short_name="d2",
            serial_number="fancy",
            model="m2",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([device1, device2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url + f"?model={device1.model}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])


class TestDeviceCustomFieldKeys(BaseTestCase):
    """Tests for the endpoints for the custom field key entries."""

    url = f"{base_url}/controller/device-custom-field-keys"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_custom_fields(self):
        """Ensure we get a list of keys."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        custom_field1 = CustomField(key="key1", value="value1", device=device)
        custom_field2 = CustomField(key="key1", value="value2", device=device)
        custom_field3 = CustomField(key="key2", value="value2", device=device)

        db.session.add_all([device, custom_field1, custom_field2, custom_field3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["key1", "key2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_customfield_key_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        custom_field1 = CustomField(key="key1", value="value1", device=device1)
        custom_field2 = CustomField(key="key1", value="value2", device=device1)
        custom_field3 = CustomField(key="key2", value="value2", device=device2)

        db.session.add_all(
            [device1, device2, custom_field1, custom_field2, custom_field3]
        )
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["key1"])

    def test_customfield_key_of_private_device_is_included_for_owner(self):
        """Ensure we give out private device data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        custom_field1 = CustomField(key="key1", value="value1", device=device1)
        custom_field2 = CustomField(key="key1", value="value2", device=device1)
        custom_field3 = CustomField(key="key2", value="value2", device=device2)

        db.session.add_all(
            [device1, device2, custom_field1, custom_field2, custom_field3]
        )
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["key1", "key2"])


class TestDeviceCustomFieldValues(BaseTestCase):
    """Tests for the endpoints for the custom field value entries."""

    url = f"{base_url}/controller/device-custom-field-values"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_custom_fields(self):
        """Ensure we get a list of values."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        custom_field1 = CustomField(key="key1", value="value1", device=device)
        custom_field2 = CustomField(key="key1", value="value2", device=device)
        custom_field3 = CustomField(key="key2", value="value2", device=device)

        db.session.add_all([device, custom_field1, custom_field2, custom_field3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["value1", "value2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_customfield_value_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        custom_field1 = CustomField(key="key1", value="value1", device=device1)
        custom_field2 = CustomField(key="key1", value="value1", device=device1)
        custom_field3 = CustomField(key="key2", value="value2", device=device2)

        db.session.add_all(
            [device1, device2, custom_field1, custom_field2, custom_field3]
        )
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["value1"])

    def test_customfield_value_of_private_device_is_included_for_owner(self):
        """Ensure we give out private device data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        custom_field1 = CustomField(key="key1", value="value1", device=device1)
        custom_field2 = CustomField(key="key1", value="value1", device=device1)
        custom_field3 = CustomField(key="key2", value="value2", device=device2)

        db.session.add_all(
            [device1, device2, custom_field1, custom_field2, custom_field3]
        )
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["value1", "value2"])


class TestDevicePropertyLabelEndpoint(BaseTestCase):
    """Tests for the label endpoint for device property labels."""

    url = f"{base_url}/controller/device-property-labels"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_device_properties(self):
        """Ensure we get a list of labels."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        device_property1 = DeviceProperty(
            label="label1", device=device, property_name="some property1"
        )
        device_property2 = DeviceProperty(
            label="label2", device=device, property_name="some property2"
        )
        device_property3 = DeviceProperty(
            label="label2", device=device, property_name="some property3"
        )

        db.session.add_all(
            [device, device_property1, device_property2, device_property3]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["label1", "label2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        device_property1 = DeviceProperty(
            label="label1", device=device1, property_name="some property1"
        )
        device_property2 = DeviceProperty(
            label="label2", device=device2, property_name="some property2"
        )
        device_property3 = DeviceProperty(
            label="label2", device=device2, property_name="some property3"
        )

        db.session.add_all(
            [device1, device2, device_property1, device_property2, device_property3]
        )
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["label1"])

    def test_entry_of_private_device_is_included_for_owner(self):
        """Ensure we give out private device data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        device_property1 = DeviceProperty(
            label="label1", device=device1, property_name="some property1"
        )
        device_property2 = DeviceProperty(
            label="label2", device=device2, property_name="some property2"
        )
        device_property3 = DeviceProperty(
            label="label2", device=device2, property_name="some property3"
        )

        db.session.add_all(
            [device1, device2, device_property1, device_property2, device_property3]
        )
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["label1", "label2"])


class TestDeviceCalibrationActionFormulaEndpoint(BaseTestCase):
    """Tests for the free text endpoint for device calibation action formulas."""

    url = f"{base_url}/controller/device-calibration-action-formulas"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of formulas."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        device_calibration1 = DeviceCalibrationAction(
            formula="f1",
            device=device,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration2 = DeviceCalibrationAction(
            formula="f2",
            device=device,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration3 = DeviceCalibrationAction(
            formula="f2",
            device=device,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )

        db.session.add_all(
            [
                device,
                contact,
                device_calibration1,
                device_calibration2,
                device_calibration3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["f1", "f2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        device_calibration1 = DeviceCalibrationAction(
            formula="f1",
            device=device1,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration2 = DeviceCalibrationAction(
            formula="f2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration3 = DeviceCalibrationAction(
            formula="f2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                device_calibration1,
                device_calibration2,
                device_calibration3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["f1"])

    def test_entry_of_private_device_is_included_for_owner(self):
        """Ensure we show data for private devices to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        device_calibration1 = DeviceCalibrationAction(
            formula="f1",
            device=device1,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration2 = DeviceCalibrationAction(
            formula="f2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration3 = DeviceCalibrationAction(
            formula="f2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                device_calibration1,
                device_calibration2,
                device_calibration3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["f1", "f2"])


class TestDeviceCalibrationActionDescriptionEndpoint(BaseTestCase):
    """Tests for the free text endpoint for device calibation action descriptions."""

    url = f"{base_url}/controller/device-calibration-action-descriptions"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of descriptions."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        device_calibration1 = DeviceCalibrationAction(
            description="d1",
            device=device,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration2 = DeviceCalibrationAction(
            description="d2",
            device=device,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration3 = DeviceCalibrationAction(
            description="d2",
            device=device,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )

        db.session.add_all(
            [
                device,
                contact,
                device_calibration1,
                device_calibration2,
                device_calibration3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["d1", "d2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        device_calibration1 = DeviceCalibrationAction(
            description="d1",
            device=device1,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration2 = DeviceCalibrationAction(
            description="d2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration3 = DeviceCalibrationAction(
            description="d2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                device_calibration1,
                device_calibration2,
                device_calibration3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["d1"])

    def test_entry_of_private_device_is_included_for_owner(self):
        """Ensure we show data for private devices to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        device_calibration1 = DeviceCalibrationAction(
            description="d1",
            device=device1,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration2 = DeviceCalibrationAction(
            description="d2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )
        device_calibration3 = DeviceCalibrationAction(
            description="d2",
            device=device2,
            contact=contact,
            current_calibration_date=datetime(2022, 11, 4, 12, 0, 0),
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                device_calibration1,
                device_calibration2,
                device_calibration3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["d1", "d2"])


class TestConfigurationLabelEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for configuration labels."""

    url = f"{base_url}/controller/configuration-labels"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_configurations(self):
        """Ensure we get a list of labels."""
        config1 = Configuration(
            label="dummy",
            is_public=True,
            is_internal=False,
        )
        config2 = Configuration(
            label="dummy",
            is_public=True,
            is_internal=False,
        )
        config3 = Configuration(
            label="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([config1, config2, config3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestGenericDeviceActionDescriptionEndpoint(BaseTestCase):
    """Tests for the free text endpoint for device action descriptions."""

    url = f"{base_url}/controller/generic-device-action-descriptions"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of descriptions."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = GenericDeviceAction(
            action_type_name="device action",
            device=device,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = GenericDeviceAction(
            action_type_name="device action",
            device=device,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = GenericDeviceAction(
            action_type_name="device action",
            device=device,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                device,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()

        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )

        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = GenericDeviceAction(
            action_type_name="device action",
            device=device1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = GenericDeviceAction(
            action_type_name="device action",
            device=device1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = GenericDeviceAction(
            action_type_name="device action",
            device=device2,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1"])

    def test_entry_of_private_device_is_included_for_owner(self):
        """Ensure we show data for private devices to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()

        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )

        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = GenericDeviceAction(
            action_type_name="device action",
            device=device1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = GenericDeviceAction(
            action_type_name="device action",
            device=device1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = GenericDeviceAction(
            action_type_name="device action",
            device=device2,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])


class TestGenericPlatformActionDescriptionEndpoint(BaseTestCase):
    """Tests for the free text endpoint for platform action descriptions."""

    url = f"{base_url}/controller/generic-platform-action-descriptions"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of descriptions."""
        platform = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                platform,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_platform_is_not_included_for_other(self):
        """Ensure we don't show data for private platforms to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()

        platform1 = Platform(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )

        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform2,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1"])

    def test_entry_of_private_platform_is_included_for_owner(self):
        """Ensure we show data for private platforms to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()

        platform1 = Platform(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )

        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform1,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = GenericPlatformAction(
            action_type_name="platform action",
            platform=platform2,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])


class TestGenericConfigurationActionDescriptionEndpoint(BaseTestCase):
    """Tests for the free text endpoint for configuration action descriptions."""

    url = f"{base_url}/controller/generic-configuration-action-descriptions"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of descriptions."""
        configuration = Configuration(
            label="dummy",
            is_public=True,
            is_internal=False,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = GenericConfigurationAction(
            action_type_name="configuration action",
            configuration=configuration,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = GenericConfigurationAction(
            action_type_name="configuration action",
            configuration=configuration,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = GenericConfigurationAction(
            action_type_name="configuration action",
            configuration=configuration,
            contact=contact,
            begin_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                configuration,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestDeviceSoftwareUpdateActionDescriptionEndpoint(BaseTestCase):
    """Tests for the free text endpoint for device software update action descriptions."""

    url = f"{base_url}/controller/device-software-update-action-descriptions"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of descriptions."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                device,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1"])

    def test_entry_of_private_device_is_included_for_owner(self):
        """Ensure we show data for private devices to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])


class TestPlatformSoftwareUpdateActionDescriptionEndpoint(BaseTestCase):
    """Tests for the free text endpoint for platform software update action descriptions."""

    url = f"{base_url}/controller/platform-software-update-action-descriptions"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of descriptions."""
        platform = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                platform,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_platform_is_not_included_for_other(self):
        """Ensure we don't show data for private platforms to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        platform1 = Platform(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1"])

    def test_entry_of_private_platform_is_included_for_owner(self):
        """Ensure we show data for private platforms to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        platform1 = Platform(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action2 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc1",
        )
        action3 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            description="desc2",
        )

        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["desc1", "desc2"])


class TestDeviceSoftwareUpdateActionRepositoryUrlEndpoint(BaseTestCase):
    """Tests for the free text endpoint for device software update action repository urls."""

    url = f"{base_url}/controller/device-software-update-action-repository-urls"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of repository urls."""
        device = Device(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="http://github",
        )
        action2 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="http://github",
        )
        action3 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="http://gitlab",
        )

        db.session.add_all(
            [
                device,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["http://github", "http://gitlab"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_device_is_not_included_for_other(self):
        """Ensure we don't show data for private devices to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action2 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action3 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo2",
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["repo1"])

    def test_entry_of_private_device_is_included_for_owner(self):
        """Ensure we show data for private devices to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        device1 = Device(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        device2 = Device(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action2 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action3 = DeviceSoftwareUpdateAction(
            software_type_name="OS",
            device=device2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo2",
        )

        db.session.add_all(
            [
                device1,
                device2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["repo1", "repo2"])


class TestPlatformSoftwareUpdateActionRepositoryUrlEndpoint(BaseTestCase):
    """Tests for the free text endpoint for platform software update action repository urls."""

    url = f"{base_url}/controller/platform-software-update-action-repository-urls"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_model_instances(self):
        """Ensure we get a list of repository urls."""
        platform = Platform(
            short_name="dummy", is_public=True, is_internal=False, is_private=False
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="http://github",
        )
        action2 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="http://github",
        )
        action3 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="http://gitlab",
        )

        db.session.add_all(
            [
                platform,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["http://github", "http://gitlab"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_entry_of_private_platform_is_not_included_for_other(self):
        """Ensure we don't show data for private platforms to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        platform1 = Platform(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action2 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action3 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo2",
        )

        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["repo1"])

    def test_entry_of_private_platform_is_included_for_owner(self):
        """Ensure we show data for private platforms to owners."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        db.session.commit()
        platform1 = Platform(
            short_name="d1", is_public=True, is_internal=False, is_private=False
        )
        platform2 = Platform(
            short_name="d2",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        contact = Contact(
            given_name="con", family_name="tact", email="contact@localhost"
        )
        action1 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action2 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform1,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo1",
        )
        action3 = PlatformSoftwareUpdateAction(
            software_type_name="OS",
            platform=platform2,
            contact=contact,
            update_date=datetime(2022, 11, 4, 12, 0, 0),
            repository_url="repo2",
        )

        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                action1,
                action2,
                action3,
            ]
        )
        db.session.commit()

        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["repo1", "repo2"])


class TestPlatformManufacturerNames(BaseTestCase):
    """Tests for the endpoints for the platform manufacturer names."""

    url = f"{base_url}/controller/platform-manufacturer-names"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_manufacturers(self):
        """Ensure we get a list of manufacturer names."""
        platform1 = Platform(
            short_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
            manufacturer_name="Platform GmbH",
        )
        platform2 = Platform(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            manufacturer_name="Platform GmbH",
        )
        platform3 = Platform(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            manufacturer_name="Alternative & Co",
        )

        db.session.add_all([platform1, platform2, platform3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["Alternative & Co", "Platform GmbH"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_manufacturer_name_of_private_platform_is_not_included_for_other(self):
        """Ensure we don't show data for private platforms to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="d1",
            manufacturer_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            manufacturer_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_manufacturer_name_of_private_platform_is_included_for_owner(self):
        """Ensure we give out private platform data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="d1",
            manufacturer_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            manufacturer_name="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])


class TestPlatformSerialNumbers(BaseTestCase):
    """Tests for the endpoints for the platform serial numbers."""

    url = f"{base_url}/controller/platform-serial-numbers"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_serialnumbers(self):
        """Ensure we get a list of serial numbers."""
        platform1 = Platform(
            short_name="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
            serial_number="23",
        )
        platform2 = Platform(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            serial_number="23",
        )
        platform3 = Platform(
            short_name="dummy XXL",
            is_public=True,
            is_internal=False,
            is_private=False,
            serial_number="69",
        )

        db.session.add_all([platform1, platform2, platform3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["23", "69"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")

    def test_serial_number_of_private_platform_is_not_included_for_other(self):
        """Ensure we don't show data for private platforms to other users."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            serial_number="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by_id=other_user.id,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_serial_number_of_private_platform_is_included_for_owner(self):
        """Ensure we give out private platform data for the owner."""
        other_contact = Contact(
            given_name="other", family_name="contact", email="other.contact@localhost"
        )
        other_user = User(subject=other_contact.email, contact=other_contact)
        db.session.add_all([other_contact, other_user])
        platform1 = Platform(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            serial_number="fancy",
            is_public=False,
            is_internal=False,
            is_private=True,
            created_by=other_user,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(other_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "fancy"])

    def test_ignore_by_ids(self):
        """Ensure we can ignore the entries that come from certain ids."""
        platform1 = Platform(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            serial_number="fancy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url + f"?ignore={platform1.id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["fancy"])

    def test_prefilter_by_short_name(self):
        """Ensure we can filter the set by a given short name."""
        platform1 = Platform(
            short_name="d1",
            serial_number="dummy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            serial_number="fancy",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url + f"?short_name={platform1.short_name}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_prefilter_by_manufacturer_name(self):
        """Ensure we can filter the set by a manufacturer name."""
        platform1 = Platform(
            short_name="d1",
            serial_number="dummy",
            manufacturer_name="m1",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            serial_number="fancy",
            manufacturer_name="m2",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(
                self.url + f"?manufacturer_name={platform1.manufacturer_name}"
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_prefilter_by_manufacturer_uri(self):
        """Ensure we can filter the set by a manufacturer name."""
        platform1 = Platform(
            short_name="d1",
            serial_number="dummy",
            manufacturer_uri="m1",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            serial_number="fancy",
            manufacturer_uri="m2",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(
                self.url + f"?manufacturer_uri={platform1.manufacturer_uri}"
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])

    def test_prefilter_by_model(self):
        """Ensure we can filter the set by a manufacturer name."""
        platform1 = Platform(
            short_name="d1",
            serial_number="dummy",
            model="m1",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        platform2 = Platform(
            short_name="d2",
            serial_number="fancy",
            model="m2",
            is_public=True,
            is_internal=False,
            is_private=False,
        )
        db.session.add_all([platform1, platform2])
        db.session.commit()
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url + f"?model={platform1.model}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy"])


class TestConfigurationCustomFieldKeys(BaseTestCase):
    """Tests for the endpoints for the configuration custom field key entries."""

    url = f"{base_url}/controller/configuration-custom-field-keys"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_custom_fields(self):
        """Ensure we get a list of keys."""
        configuration = Configuration(
            label="dummy",
            is_public=True,
            is_internal=False,
        )
        custom_field1 = ConfigurationCustomField(
            key="key1", value="value1", configuration=configuration
        )
        custom_field2 = ConfigurationCustomField(
            key="key1", value="value2", configuration=configuration
        )
        custom_field3 = ConfigurationCustomField(
            key="key2", value="value2", configuration=configuration
        )

        db.session.add_all([configuration, custom_field1, custom_field2, custom_field3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["key1", "key2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestConfigurationCustomFieldValues(BaseTestCase):
    """Tests for the endpoints for the configuration custom field value entries."""

    url = f"{base_url}/controller/configuration-custom-field-values"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_custom_fields(self):
        """Ensure we get a list of values."""
        configuration = Configuration(
            label="dummy",
            is_public=True,
            is_internal=False,
        )
        custom_field1 = ConfigurationCustomField(
            key="key1", value="value1", configuration=configuration
        )
        custom_field2 = ConfigurationCustomField(
            key="key1", value="value2", configuration=configuration
        )
        custom_field3 = ConfigurationCustomField(
            key="key2", value="value2", configuration=configuration
        )

        db.session.add_all([configuration, custom_field1, custom_field2, custom_field3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["value1", "value2"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteLabelEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site labels."""

    url = f"{base_url}/controller/site-labels"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            label="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            label="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            label="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteStreetEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site streets."""

    url = f"{base_url}/controller/site-streets"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            street="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            street="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            street="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteStreetNumberEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site street numbers."""

    url = f"{base_url}/controller/site-street-numbers"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            street_number="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            street_number="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            street_number="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteCityEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site cities."""

    url = f"{base_url}/controller/site-cities"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            city="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            city="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            city="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteZipCodeEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site zip codes."""

    url = f"{base_url}/controller/site-zip-codes"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            zip_code="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            zip_code="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            zip_code="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteCountryEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site countries."""

    url = f"{base_url}/controller/site-countries"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            country="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            country="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            country="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteBuildingEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site buildings."""

    url = f"{base_url}/controller/site-buildings"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            building="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            building="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            building="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestSiteRoomEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for site rooms."""

    url = f"{base_url}/controller/site-rooms"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, [])

    def test_get_for_three_sites(self):
        """Ensure we get a list of sites."""
        site1 = Site(
            room="dummy",
            is_public=True,
            is_internal=False,
        )
        site2 = Site(
            room="dummy",
            is_public=True,
            is_internal=False,
        )
        site3 = Site(
            room="no dummy",
            is_public=True,
            is_internal=False,
        )

        db.session.add_all([site1, site2, site3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["dummy", "no dummy"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")


class TestContactOrganizationEndpoint(BaseTestCase):
    """Tests for the free text field endpoint for contacts organization."""

    url = f"{base_url}/controller/contact-organizations"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal",
            family_name="contact",
            email="normal.contact@localhost",
        )
        self.normal_user = User(
            subject=self.normal_contact.email, contact=self.normal_contact
        )
        db.session.add_all([self.normal_contact, self.normal_user])
        db.session.commit()

    def test_get_without_user(self):
        """Ensure that we need a user."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_get_empty(self):
        """Ensure we can get an empty response."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        # We have a contact (self.normal_contact), but there are no
        # organizations.
        self.assertEqual(data, [])

    def test_get_for_three_contacts(self):
        """Ensure we get a list of contacts."""
        self.normal_contact.organization = "Normal organization"
        contact2 = Contact(
            given_name="second",
            family_name="contact",
            email="second@contacts",
            organization="Normal organization",
        )
        contact3 = Contact(
            given_name="third",
            family_name="contact",
            email="third@contacts",
            organization="Fancy organization",
        )

        db.session.add_all([self.normal_contact, contact2, contact3])
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json["data"]
        self.assertEqual(data, ["Fancy organization", "Normal organization"])

    def test_endpoint_is_in_openapi_spec(self):
        """Ensure that we documented that endpoint in the openAPI."""
        endpoint_url = self.url.replace(base_url, "")
        openapi_url = url_for("docs.openapi_json")

        response = self.client.get(openapi_url)
        openapi_specs = response.json
        paths = openapi_specs["paths"]
        self.assertIn(endpoint_url, paths.keys())
        path_endpoint = paths[endpoint_url]
        self.assertIn("get", path_endpoint.keys())
        get_endpoint = path_endpoint["get"]

        # We have an entry for the responses. And we document both
        # the success response, as well as the error responses.
        self.assertIn("responses", get_endpoint.keys())
        self.assertTrue(get_endpoint["responses"])
        self.assertIn("200", get_endpoint["responses"].keys())
        self.assertIn("401", get_endpoint["responses"].keys())

        # In the list of tags is Controller.
        self.assertIn("tags", get_endpoint.keys())
        self.assertIn("Controller", get_endpoint["tags"])

        # And we have both description and operationId
        required = ["description", "operationId"]
        for field in required:
            self.assertIn(field, get_endpoint.keys())
            self.assertTrue(get_endpoint[field] is not None)
            self.assertTrue(get_endpoint[field] != "")
