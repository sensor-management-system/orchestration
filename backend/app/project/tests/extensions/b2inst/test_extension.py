# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test classes for the b2inst extension."""
import json
from unittest.mock import patch

from flask import current_app
from requests import HTTPError

from project.api.helpers.errors import BadRequestError
from project.api.models import Configuration, Contact, Device, Platform, Site
from project.api.models.base_model import db
from project.extensions.b2inst import schemas
from project.extensions.instances import pidinst
from project.tests.base import BaseTestCase


class FakeResponse:
    """Helper class to have a fake response to mock the requests calls."""

    def __init__(self, json=None):
        """Init the object."""
        self._json = json

    def json(self):
        """Return the json value."""
        return self._json

    def raise_for_status(self):
        """
        Raise an exception if the status code is not good.

        Not implemented yet.
        """
        pass

    @property
    def ok(self):
        """Return true to show that the request was successful."""
        return True


class TestB2Inst(BaseTestCase):
    """Test class for the B2Inst class."""

    def test_create_pid_device_failed_due_to_validation_error(self):
        """Ensure we raise a BadRequestError if the requests to b2inst failed."""
        instrument = Device(short_name="Test device")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community, patch.object(
            b2inst, "_create_draft"
        ) as create_draft, patch.object(b2inst, "_publish_draft") as publish_draft:
            find_community.return_value = "1234-5678"
            create_draft.return_value = {"id": "42"}
            publish_draft.side_effect = HTTPError(
                request=None, response=FakeResponse({"message": "Validation failed."})
            )

            with self.assertRaises(BadRequestError):
                b2inst.create_pid(instrument)

    def test_create_pid_device_failed_due_to_http_error(self):
        """Ensure we reraise the HTTPError if we got no message in the error."""
        instrument = Device(short_name="Test device")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community, patch.object(
            b2inst, "_create_draft"
        ) as create_draft, patch.object(b2inst, "_publish_draft") as publish_draft:
            find_community.return_value = "1234-5678"
            create_draft.return_value = {"id": "42"}
            publish_draft.side_effect = HTTPError(
                request=None, response=FakeResponse({"Reason": "Validation failed."})
            )

            with self.assertRaises(HTTPError):
                b2inst.create_pid(instrument)

    def test_create_pid_device_failed_due_to_different_error(self):
        """Ensure we raise a the same exception as we got."""
        instrument = Device(short_name="Test device")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        class ExampleException(Exception):
            pass

        with patch.object(b2inst, "_find_community_id") as find_community, patch.object(
            b2inst, "_create_draft"
        ) as create_draft, patch.object(b2inst, "_publish_draft") as publish_draft:
            find_community.return_value = "1234-5678"
            create_draft.return_value = {"id": "42"}
            publish_draft.side_effect = ExampleException()

            with self.assertRaises(ExampleException):
                b2inst.create_pid(instrument)

    def test_create_pid_device(self):
        """Ensure we can create a pid for a device."""
        instrument = Device(short_name="Test device")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community, patch.object(
            b2inst, "_create_draft"
        ) as create_draft, patch.object(
            b2inst, "_publish_draft"
        ) as publish_draft, patch.object(
            b2inst, "_get_record_data"
        ) as get_record_data:
            find_community.return_value = "1234-5678"
            create_draft.return_value = {"id": "42"}
            publish_draft.return_value = None
            get_record_data.return_value = {
                "metadata": {"ePIC_PID": "http://hdl.handle.net/42.123/4567890"}
            }

            pid = b2inst.create_pid(instrument)

            find_community.assert_called_once()
            create_draft.assert_called_once()
            self.assertEqual(create_draft.call_args.args[0].name, "Test device")
            publish_draft.assert_called_with("42")
            get_record_data.assert_called_with("42")

        self.assertEqual(pid, "42.123/4567890")
        # We set the b2inst record id field in this process.
        self.assertEqual(instrument.b2inst_record_id, "42")
        # But we don't set the persistent identifier.
        self.assertIsNone(instrument.persistent_identifier)

    def test_create_pid_platform(self):
        """Ensure we can create a pid for a platform."""
        instrument = Platform(short_name="Test platform")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community, patch.object(
            b2inst, "_create_draft"
        ) as create_draft, patch.object(
            b2inst, "_publish_draft"
        ) as publish_draft, patch.object(
            b2inst, "_get_record_data"
        ) as get_record_data:
            find_community.return_value = "1234-5678"
            create_draft.return_value = {"id": "42"}
            publish_draft.return_value = None
            get_record_data.return_value = {
                "metadata": {"ePIC_PID": "http://hdl.handle.net/42.123/4567890"}
            }

            pid = b2inst.create_pid(instrument)

            find_community.assert_called_once()
            create_draft.assert_called_once()
            self.assertEqual(create_draft.call_args.args[0].name, "Test platform")
            publish_draft.assert_called_with("42")
            get_record_data.assert_called_with("42")

        self.assertEqual(pid, "42.123/4567890")
        # We set the b2inst record id field in this process.
        self.assertEqual(instrument.b2inst_record_id, "42")
        # But we don't set the persistent identifier.
        self.assertIsNone(instrument.persistent_identifier)

    def test_create_pid_configuration(self):
        """Ensure we can create a pid for a configuration."""
        instrument = Configuration(label="Test configuration")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community, patch.object(
            b2inst, "_create_draft"
        ) as create_draft, patch.object(
            b2inst, "_publish_draft"
        ) as publish_draft, patch.object(
            b2inst, "_get_record_data"
        ) as get_record_data:
            find_community.return_value = "1234-5678"
            create_draft.return_value = {"id": "42"}
            publish_draft.return_value = None
            get_record_data.return_value = {
                "metadata": {"ePIC_PID": "http://hdl.handle.net/42.123/4567890"}
            }

            pid = b2inst.create_pid(instrument)

            find_community.assert_called_once()
            create_draft.assert_called_once()
            self.assertEqual(create_draft.call_args.args[0].name, "Test configuration")
            publish_draft.assert_called_with("42")
            get_record_data.assert_called_with("42")

        self.assertEqual(pid, "42.123/4567890")
        # We set the b2inst record id field in this process.
        self.assertEqual(instrument.b2inst_record_id, "42")
        # But we don't set the persistent identifier.
        self.assertIsNone(instrument.persistent_identifier)

    def test_update_external_metadata_device(self):
        """Ensure we can update the external metadata for a device."""
        instrument = Device(short_name="Test device", b2inst_record_id="42")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community:
            find_community.return_value = "1234-5678"
            with patch("requests.get") as requests_get:
                requests_get.return_value = FakeResponse({"metadata": {}})
                with patch("requests.patch") as requests_patch:
                    requests_patch.return_value = FakeResponse()
                    b2inst.update_external_metadata(instrument, run_async=False)
                    requests_patch.assert_called_once()
                    args = requests_patch.call_args.args
                    url = args[0]
                    self.assertTrue("api/records/42" in url)
                    kwargs = requests_patch.call_args.kwargs
                    data = json.loads(kwargs["data"])
                    name_change = [x for x in data if x["path"] == "/name"][0]
                    self.assertEqual(name_change["value"], "Test device")

    def test_update_external_metadata_platform(self):
        """Ensure we can update the external metadata for a platform."""
        instrument = Platform(short_name="Test platform", b2inst_record_id="42")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community:
            find_community.return_value = "1234-5678"
            with patch("requests.get") as requests_get:
                requests_get.return_value = FakeResponse({"metadata": {}})
                with patch("requests.patch") as requests_patch:
                    requests_patch.return_value = FakeResponse()
                    b2inst.update_external_metadata(instrument, run_async=False)
                    requests_patch.assert_called_once()
                    args = requests_patch.call_args.args
                    url = args[0]
                    self.assertTrue("api/records/42" in url)
                    kwargs = requests_patch.call_args.kwargs
                    data = json.loads(kwargs["data"])
                    name_change = [x for x in data if x["path"] == "/name"][0]
                    self.assertEqual(name_change["value"], "Test platform")

    def test_update_external_metadata_configuration(self):
        """Ensure we can update the external metadata for a configuration."""
        instrument = Configuration(label="Test configuration", b2inst_record_id="42")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch.object(b2inst, "_find_community_id") as find_community:
            find_community.return_value = "1234-5678"
            with patch("requests.get") as requests_get:
                requests_get.return_value = FakeResponse({"metadata": {}})
                with patch("requests.patch") as requests_patch:
                    requests_patch.return_value = FakeResponse()
                    b2inst.update_external_metadata(instrument, run_async=False)
                    requests_patch.assert_called_once()
                    args = requests_patch.call_args.args
                    url = args[0]
                    self.assertTrue("api/records/42" in url)
                    kwargs = requests_patch.call_args.kwargs
                    data = json.loads(kwargs["data"])
                    name_change = [x for x in data if x["path"] == "/name"][0]
                    self.assertEqual(name_change["value"], "Test configuration")

    def test_get_communities(self):
        """Ensure we can get a list of communities."""
        b2inst = pidinst.b2inst
        with patch("requests.get") as requests_get:
            requests_get.return_value = FakeResponse(
                {
                    "hits": {
                        "hits": [
                            {
                                "id": "1",
                                "name": "EUDAT",
                            },
                            {"id": "2", "name": "AWI"},
                        ]
                    }
                }
            )
            communities = b2inst._get_communities()
            requests_get.assert_called_once()
            url = requests_get.call_args.args[0]
            self.assertTrue("api/communities" in url)

        self.assertEqual(
            communities, [{"id": "1", "name": "EUDAT"}, {"id": "2", "name": "AWI"}]
        )

    def test_find_community_id(self):
        """Ensure we can find the community id for our community name."""
        b2inst = pidinst.b2inst
        with patch.object(b2inst, "_get_communities") as get_communities:
            get_communities.return_value = [
                {
                    "id": "1",
                    "name": "EUDAT",
                },
                {"id": "2", "name": "AWI"},
            ]

            eudat_id = b2inst._find_community_id("EUDAT")
            self.assertEqual(eudat_id, "1")
            awi_id = b2inst._find_community_id("AWI")
            self.assertEqual(awi_id, "2")
            none_id = b2inst._find_community_id("something different")
            self.assertIsNone(none_id)

    def test_create_draft(self):
        """Ensure we can make requests to create drafts."""
        b2inst = pidinst.b2inst
        draft = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            name="test name",
            Name="test Name",
            Description="test description",
            Owner=[],
            InstrumentType=[],
            LandingPage="http://somewhere.in/the/web",
            Manufacturer=[],
            Model=None,
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[],
            SchemaVersion="1.0.0",
        )

        with patch("requests.post") as requests_post:
            requests_post.return_value = FakeResponse({"id": "42"})
            result = b2inst._create_draft(draft)
            self.assertEqual(result, {"id": "42"})
            requests_post.assert_called_once()
            url = requests_post.call_args.args[0]
            self.assertTrue("api/records" in url)
            data = requests_post.call_args.kwargs["json"]
            expected_data = {
                "community": "A",
                "open_access": True,
                "name": "test name",
                "Name": "test Name",
                "Description": "test description",
                "Owner": [],
                "LandingPage": "http://somewhere.in/the/web",
                "Manufacturer": [],
                "Date": [],
                "AlternateIdentifier": [],
                "SchemaVersion": "1.0.0",
            }
            self.assertEqual(data, expected_data)

    def test_publish_draft(self):
        """Ensure we can publish the draft."""
        b2inst = pidinst.b2inst
        draft_id = "42"
        with patch("requests.patch") as requests_patch:
            requests_patch.return_value = FakeResponse()
            b2inst._publish_draft(draft_id)
            args = requests_patch.call_args.args
            url = args[0]
            self.assertTrue("api/records/42/draft" in url)
            kwargs = requests_patch.call_args.kwargs
            data = json.loads(kwargs["data"])
            expected_data = [
                {
                    "op": "add",
                    "path": "/publication_state",
                    "value": "submitted",
                }
            ]
            self.assertEqual(data, expected_data)

    def test_get_record_data(self):
        """Ensure we can get information about the record."""
        b2inst = pidinst.b2inst
        record_id = "42"
        with patch("requests.get") as requests_get:
            requests_get.return_value = FakeResponse({"id": "42"})
            result = b2inst._get_record_data(record_id)
            args = requests_get.call_args.args
            url = args[0]
            self.assertTrue("api/records/42" in url)
            # No further processing of the response.
            self.assertEqual(result, {"id": "42"})

    def test_check_availability(self):
        """Ensure we can check if the service is running or not."""
        b2inst = pidinst.b2inst
        with patch("requests.get") as requests_get:
            requests_get.return_value = FakeResponse()
            b2inst.check_availability()
            requests_get.assert_called_once()
            args = requests_get.call_args.args
            url = args[0]
            self.assertTrue("api" in url)

    def test_has_external_metadata(self):
        """Test the has_external_metadata method."""
        b2inst = pidinst.b2inst
        test_cases = [
            (Device(), False),
            (Device(b2inst_record_id="42"), True),
            (Platform(), False),
            (Platform(b2inst_record_id="43"), True),
            (Configuration(), False),
            (Configuration(b2inst_record_id="44"), True),
            (Site(), False),
            (Contact(), False),
        ]

        for test_value, expected_result in test_cases:
            result = b2inst.has_external_metadata(test_value)
            self.assertEqual(result, expected_result)

    def test_get_record_frontend_url(self):
        """Ensure we can get the frontend url for a record."""
        current_app.config.update({"B2INST_URL": "https://b2inst-test.gwdg.de"})
        b2inst = pidinst.b2inst
        result = b2inst.get_record_frontend_url("123")
        self.assertEqual(result, "https://b2inst-test.gwdg.de/records/123")
