"""Tests for the custom field endpoints."""

import json

from project import base_url
from project.api.models.base_model import db
from project.api.models.customfield import CustomField
from project.api.models.device import Device
from project.tests.base import BaseTestCase, create_token, query_result_to_list


class TestCustomFieldServices(BaseTestCase):
    """Test customfields."""
    url = base_url + "/customfields"

    def test_get_public_customfields(self):
        """Ensure that we can get a list of public customfields."""
        device1 = Device(
            short_name="Just a device",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
            short_name="Another device",
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device1,
        )
        customfield2 = CustomField(
            key="UFZ", value="https://www.ufz.de", device=device1,
        )
        customfield3 = CustomField(
            key="PIK", value="https://www.pik-potsdam.de", device=device2,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.add(customfield3)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/customfields", content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_customfields(self):
        """Ensure that we can get a list of internal customfields only with a valid jwt."""
        device1 = Device(
            short_name="Just a device",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        device2 = Device(
            short_name="Another device",
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device1,
        )
        customfield2 = CustomField(
            key="UFZ", value="https://www.ufz.de", device=device1,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url, content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)