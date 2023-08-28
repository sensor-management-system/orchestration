# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test cases for the Pidinst extension."""

from unittest.mock import Mock, patch

import requests
from flask import current_app

from project.api.models import Configuration, Device, Platform
from project.api.models.base_model import db
from project.extensions.instances import pidinst
from project.tests.base import BaseTestCase


class ActiveStubB2Inst:
    """Dummy implementation that has the b2inst active."""

    @property
    def token(self):
        """Return the token."""
        return "abc"

    def create_pid(self, instrument):
        """Return a pid for the instrument."""
        return "42/1234567890"

    def check_availability(self):
        """Raise an exception of the service is not there."""
        pass


class InactiveStubB2Inst:
    """Dummy implementation that has the b2inst inactive."""

    @property
    def token(self):
        """Don't return  token."""
        return None

    def create_pid(self, instrument):
        """Don't return a pid."""
        return None


class WrapperStubB2Inst:
    """Wrapper dummy test class that reuses some of the existing logic."""

    def __init__(self, inner, token):
        """Init the object."""
        self.inner = inner
        self.token = token

    def has_external_metadata(self, instrument):
        """Return true if we have external metadata."""
        return self.inner.has_external_metadata(instrument)

    def update_external_metadata(self, instrument):
        """Update the external metadata."""
        return self.instrument.update_external_metadata(instrument)


class TestPidinst(BaseTestCase):
    """Test class for the pidisnt extension."""

    def setUp(self):
        """Store the original pid mechanisms."""
        super().setUp()
        self.original_b2inst = pidinst.b2inst

    def tearDown(self):
        """Restore the original pid mechanisms."""
        pidinst.b2inst = self.original_b2inst
        super().tearDown()

    def test_create_pid_via_b2inst(self):
        """Test that we can get the pids via a fake b2inst."""
        test_device = Device(short_name="test device")
        db.session.add(test_device)
        db.session.commit()

        pidinst.b2inst = ActiveStubB2Inst()
        persistent_identifier = pidinst.create_pid(test_device)
        self.assertEqual(persistent_identifier, "42/1234567890")

    def test_create_device_pid_via_normal_pid(self):
        """Test that we can get the pids for devices via a pid service."""
        test_device = Device(short_name="test device")
        db.session.add(test_device)
        db.session.commit()
        frontend_url = current_app.config["SMS_FRONTEND_URL"]
        pidinst.b2inst = InactiveStubB2Inst()
        with patch.object(pidinst.pid, "create") as mock:
            mock.return_value = "10/4213567890"
            persistent_identifier = pidinst.create_pid(test_device)
            mock.assert_called_with(f"{frontend_url}/devices/{test_device.id}")
        self.assertEqual(persistent_identifier, "10/4213567890")

    def test_create_platform_pid_via_normal_pid(self):
        """Test that we can get the pids for platforms via a pid service."""
        test_platform = Platform(short_name="test platform")
        db.session.add(test_platform)
        db.session.commit()
        frontend_url = current_app.config["SMS_FRONTEND_URL"]
        pidinst.b2inst = InactiveStubB2Inst()
        with patch.object(pidinst.pid, "create") as mock:
            mock.return_value = "10/4213567890"
            persistent_identifier = pidinst.create_pid(test_platform)
            mock.assert_called_with(f"{frontend_url}/platforms/{test_platform.id}")
        self.assertEqual(persistent_identifier, "10/4213567890")

    def test_create_configuration_pid_via_normal_pid(self):
        """Test that we can get the pids for configurations via a pid service."""
        test_configuration = Configuration(label="test configuration")
        db.session.add(test_configuration)
        db.session.commit()
        frontend_url = current_app.config["SMS_FRONTEND_URL"]
        pidinst.b2inst = InactiveStubB2Inst()
        with patch.object(pidinst.pid, "create") as mock:
            mock.return_value = "10/4213567890"
            persistent_identifier = pidinst.create_pid(test_configuration)
            mock.assert_called_with(
                f"{frontend_url}/configurations/{test_configuration.id}"
            )
        self.assertEqual(persistent_identifier, "10/4213567890")

    def test_check_availability_b2inst(self):
        """Ensure we can check the availability for b2inst via the pidinst extension."""
        pidinst.b2inst = ActiveStubB2Inst()
        with patch.object(pidinst.b2inst, "check_availability") as mock:
            mock.return_value = None
            pidinst.check_availability()
            mock.assert_called_once()

    def test_check_not_avialable_b2inst(self):
        """Ensure we get an error if the b2inst should be there, but isn"t."""
        pidinst.b2inst = ActiveStubB2Inst()
        with patch.object(pidinst.b2inst, "check_availability") as mock:
            mock.side_effect = requests.exceptions.HTTPError("Not there")
            with self.assertRaises(requests.exceptions.HTTPError):
                pidinst.check_availability()
            mock.assert_called_once()

    def test_check_availability_normal_pid(self):
        """Ensure we can check the availability for normal pid via the pidinst extension."""
        pidinst.b2inst = InactiveStubB2Inst()
        with patch.object(pidinst.pid, "list") as mock:
            mock.side_effect = requests.exceptions.HTTPError("Not there")
            with self.assertRaises(requests.exceptions.HTTPError):
                pidinst.check_availability()
            mock.assert_called_once()

    def test_has_no_external_metadata_in_b2inst(self):
        """Ensure we don't have external metadata to care if we don't have the b2inst record."""
        pidinst.b2inst = WrapperStubB2Inst(pidinst.b2inst, token="abc")
        test_device = Device(short_name="test device")
        db.session.add(test_device)
        db.session.commit()

        self.assertFalse(pidinst.has_external_metadata(test_device))

    def test_has_external_metadata_in_b2inst(self):
        """Ensure we know that we have external metadata if we have the b2inst record."""
        pidinst.b2inst = WrapperStubB2Inst(pidinst.b2inst, token="abc")
        test_device = Device(short_name="test device", b2inst_record_id="foo")
        db.session.add(test_device)
        db.session.commit()

        self.assertTrue(pidinst.has_external_metadata(test_device))

    def test_has_no_external_metadata_in_pid(self):
        """Ensure we don't have external metadata to update if we use just the normal pid server."""
        pidinst.b2inst = InactiveStubB2Inst()
        test_device = Device(short_name="test device", b2inst_record_id="foo")
        db.session.add(test_device)
        db.session.commit()

        self.assertFalse(pidinst.has_external_metadata(test_device))

    def test_update_external_metadata_in_b2inst(self):
        """Ensure we can ask to update the extenral metadata if we have the b2inst record."""
        pidinst.b2inst = WrapperStubB2Inst(pidinst.b2inst, token="abc")
        test_device = Device(short_name="test device", b2inst_record_id="foo")
        db.session.add(test_device)
        db.session.commit()

        with patch.object(pidinst.b2inst, "update_external_metadata") as mock:
            mock.return_value = None
            pidinst.update_external_metadata(test_device)
            mock.assert_called_once()

    def test_update_external_metadata_pid(self):
        """Ensure we could update external metadata using the normal pid handle, but nothing happens."""
        pidinst.b2inst = InactiveStubB2Inst()
        pidinst.pid = Mock()

        test_device = Device(short_name="test device", b2inst_record_id="foo")
        db.session.add(test_device)
        db.session.commit()

        pidinst.update_external_metadata(test_device)
        self.assertEqual(pidinst.pid.method_calls, [])
