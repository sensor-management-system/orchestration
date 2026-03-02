# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test classes for the b2inst extension."""

from unittest.mock import patch

from flask import current_app
from requests import HTTPError

from project.api.helpers.errors import BadRequestError
from project.api.models import Configuration, Contact, Device, Platform, Site
from project.api.models.base_model import db
from project.extensions.instances import pidinst
from project.tests.base import BaseTestCase


class TestB2Inst(BaseTestCase):
    """Test class for the B2Inst class."""

    def test_create_pid_device_failed_due_to_validation_error(self):
        """Ensure we raise a BadRequestError if the requests to b2inst failed."""
        instrument = Device(short_name="Test device")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch(
            "project.extensions.b2inst.client.B2InstClient.create_draft_record"
        ) as create_draft_record, patch.object(
            b2inst, "_find_community_id"
        ) as find_community_id, patch(
            "project.extensions.b2inst.client.B2InstClient.add_communities"
        ) as add_communities, patch(
            "project.extensions.b2inst.client.B2InstClient.publish_record"
        ) as publish_record:
            create_draft_record.return_value = {"id": "42"}
            find_community_id.return_value = "1234-5678"
            add_communities.return_value = {}
            publish_record.side_effect = HTTPError()

            with self.assertRaises(BadRequestError):
                b2inst.create_pid(instrument)

    def test_create_pid_device(self):
        """Ensure we can create a pid for a device."""
        instrument = Device(short_name="Test device")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch(
            "project.extensions.b2inst.client.B2InstClient.create_draft_record"
        ) as create_draft_record, patch.object(
            b2inst, "_find_community_id"
        ) as find_community_id, patch(
            "project.extensions.b2inst.client.B2InstClient.add_communities"
        ) as add_communities, patch(
            "project.extensions.b2inst.client.B2InstClient.publish_record"
        ) as publish_record:
            create_draft_record.return_value = {"id": "42"}
            find_community_id.return_value = "1234-5678"
            add_communities.return_value = {}
            publish_record.return_value = {
                "metadata": {"Identifier": {"identifierValue": "42.123/4567890"}}
            }
            pid = b2inst.create_pid(instrument)

            find_community_id.assert_called_once()
            create_draft_record.assert_called_once()
            self.assertEqual(
                create_draft_record.call_args.args[0]["metadata"]["Name"], "Test device"
            )
            publish_record.assert_called_with("42")

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

        with patch(
            "project.extensions.b2inst.client.B2InstClient.create_draft_record"
        ) as create_draft_record, patch.object(
            b2inst, "_find_community_id"
        ) as find_community_id, patch(
            "project.extensions.b2inst.client.B2InstClient.add_communities"
        ) as add_communities, patch(
            "project.extensions.b2inst.client.B2InstClient.publish_record"
        ) as publish_record:
            create_draft_record.return_value = {"id": "42"}
            find_community_id.return_value = "1234-5678"
            add_communities.return_value = {}
            publish_record.return_value = {
                "metadata": {"Identifier": {"identifierValue": "42.123/4567890"}}
            }

            pid = b2inst.create_pid(instrument)

            find_community_id.assert_called_once()
            create_draft_record.assert_called_once()
            self.assertEqual(
                create_draft_record.call_args.args[0]["metadata"]["Name"],
                "Test platform",
            )
            publish_record.assert_called_with("42")

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

        with patch(
            "project.extensions.b2inst.client.B2InstClient.create_draft_record"
        ) as create_draft_record, patch.object(
            b2inst, "_find_community_id"
        ) as find_community_id, patch(
            "project.extensions.b2inst.client.B2InstClient.add_communities"
        ) as add_communities, patch(
            "project.extensions.b2inst.client.B2InstClient.publish_record"
        ) as publish_record:
            create_draft_record.return_value = {"id": "42"}
            find_community_id.return_value = "1234-5678"
            add_communities.return_value = {}
            publish_record.return_value = {
                "metadata": {"Identifier": {"identifierValue": "42.123/4567890"}}
            }

            pid = b2inst.create_pid(instrument)

            find_community_id.assert_called_once()
            create_draft_record.assert_called_once()
            self.assertEqual(
                create_draft_record.call_args.args[0]["metadata"]["Name"],
                "Test configuration",
            )
            publish_record.assert_called_with("42")

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

        with patch(
            "project.extensions.b2inst.client.B2InstClient.create_new_draft"
        ) as create_new_draft, patch(
            "project.extensions.b2inst.client.B2InstClient.update_draft"
        ) as update_draft, patch(
            "project.extensions.b2inst.client.B2InstClient.publish_record"
        ) as publish_record:
            create_new_draft.return_value = {}
            update_draft.return_value = {}
            publish_record.return_value = {}

            b2inst.update_external_metadata(instrument, run_async=False)

            create_new_draft.assert_called_with("42")
            update_draft.assert_called_once()
            args = update_draft.call_args.args
            record_id = args[0]
            self.assertEqual(record_id, "42")
            draft_data = args[1]
            self.assertEqual(draft_data["metadata"]["Name"], "Test device")
            publish_record.assert_called_with("42")

    def test_update_external_metadata_platform(self):
        """Ensure we can update the external metadata for a platform."""
        instrument = Platform(short_name="Test platform", b2inst_record_id="42")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch(
            "project.extensions.b2inst.client.B2InstClient.create_new_draft"
        ) as create_new_draft, patch(
            "project.extensions.b2inst.client.B2InstClient.update_draft"
        ) as update_draft, patch(
            "project.extensions.b2inst.client.B2InstClient.publish_record"
        ) as publish_record:
            create_new_draft.return_value = {}
            update_draft.return_value = {}
            publish_record.return_value = {}

            b2inst.update_external_metadata(instrument, run_async=False)

            create_new_draft.assert_called_with("42")
            update_draft.assert_called_once()
            args = update_draft.call_args.args
            record_id = args[0]
            self.assertEqual(record_id, "42")
            draft_data = args[1]
            self.assertEqual(draft_data["metadata"]["Name"], "Test platform")
            publish_record.assert_called_with("42")

    def test_update_external_metadata_configuration(self):
        """Ensure we can update the external metadata for a configuration."""
        instrument = Configuration(label="Test configuration", b2inst_record_id="42")
        db.session.add(instrument)
        db.session.commit()

        b2inst = pidinst.b2inst

        with patch(
            "project.extensions.b2inst.client.B2InstClient.create_new_draft"
        ) as create_new_draft, patch(
            "project.extensions.b2inst.client.B2InstClient.update_draft"
        ) as update_draft, patch(
            "project.extensions.b2inst.client.B2InstClient.publish_record"
        ) as publish_record:
            create_new_draft.return_value = {}
            update_draft.return_value = {}
            publish_record.return_value = {}

            b2inst.update_external_metadata(instrument, run_async=False)

            create_new_draft.assert_called_with("42")
            update_draft.assert_called_once()
            args = update_draft.call_args.args
            record_id = args[0]
            self.assertEqual(record_id, "42")
            draft_data = args[1]
            self.assertEqual(draft_data["metadata"]["Name"], "Test configuration")
            publish_record.assert_called_with("42")

    def test_find_community_id(self):
        """Ensure we can find the community id for our community name."""
        b2inst = pidinst.b2inst
        with patch(
            "project.extensions.b2inst.client.B2InstClient.get_communities"
        ) as get_communities:
            get_communities.return_value = {
                "hits": {
                    "hits": [
                        {
                            "id": "1",
                            "metadata": {
                                "title": "EUDAT",
                            },
                        },
                        {"id": "2", "metadata": {"title": "AWI"}},
                    ]
                }
            }

            eudat_id = b2inst._find_community_id("EUDAT")
            self.assertEqual(eudat_id, "1")
            awi_id = b2inst._find_community_id("AWI")
            self.assertEqual(awi_id, "2")
            none_id = b2inst._find_community_id("something different")
            self.assertIsNone(none_id)

    def test_check_availability(self):
        """Ensure we can check if the service is running or not."""
        b2inst = pidinst.b2inst
        with patch("project.extensions.b2inst.client.B2InstClient.ping") as ping:
            ping.return_value = {}
            b2inst.check_availability()
            ping.assert_called_once()

    def test_check_availability_with_error(self):
        """Ensure we get an exception if the availability fails."""
        b2inst = pidinst.b2inst
        with patch("project.extensions.b2inst.client.B2InstClient.ping") as ping:
            ping.side_effect = Exception("problem")

            with self.assertRaises(Exception):
                b2inst.check_availability()

            ping.assert_called_once()

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
