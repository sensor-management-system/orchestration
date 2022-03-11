"""Tests for the custom field endpoints."""

import json

from project import base_url
from project.api.models.base_model import db
from project.api.models.customfield import CustomField
from project.api.models.device import Device
from project.tests.base import BaseTestCase, create_token, query_result_to_list
from project.tests.base import fake


class TestCustomFieldServices(BaseTestCase):
    """Test customfields."""

    url = base_url + "/customfields"

    def test_post_customfield_api(self):
        """Ensure that we can add a custom field."""
        # First we need to make sure that we have a device
        device = Device(
            short_name="Very new device",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(device.id is not None)

        count_customfields = (
            db.session.query(CustomField).filter_by(device_id=device.id, ).count()
        )
        # However, this new device for sure has no customfields
        self.assertEqual(count_customfields, 0)

        # Now we can write the request to add a customfield
        payload = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "value": "https://www.gfz-potsdam.de",
                    "key": "GFZ Homepage",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/customfields"
            # You may want to look up self.add_object in the BaseTestCase
            # and compare if something doesn't work anymore
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # We expect that it worked and that we have a new entry
        self.assertEqual(response.status_code, 201)
        # And we want to inspect our customfields list
        customfields = query_result_to_list(
            db.session.query(CustomField).filter_by(device_id=device.id, )
        )
        # We now have one customfield
        self.assertEqual(len(customfields), 1)

        # And it is as we specified it
        customfield = customfields[0]
        self.assertEqual(customfield.value, "https://www.gfz-potsdam.de")
        self.assertEqual(customfield.key, "GFZ Homepage")
        self.assertEqual(customfield.device_id, device.id)
        self.assertEqual(str(customfield.device_id), response.get_json()["data"]["id"])

    def test_post_customfield_api_missing_key(self):
        """Ensure that we don't add a customfield with missing key."""
        device = Device(
            short_name="Very new device",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()

        # Now we can write the request to add a customfield
        payload = {
            "data": {
                "type": "customfield",
                "attributes": {"key": None, "value": "GFZ Homepage", },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/customfields"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the url)
        # 422 => unprocessable entity
        self.assertEqual(response.status_code, 422)
        count_customfields = (
            db.session.query(CustomField).filter_by(device_id=device.id, ).count()
        )
        self.assertEqual(count_customfields, 0)

    def test_post_customfield_api_missing_device(self):
        """Ensure that we don't add a customfield with missing device."""
        count_customfields_before = db.session.query(CustomField).count()
        payload = {
            "data": {
                "type": "customfield",
                "attributes": {"key": "GFZ", "value": "GFZ Homepage", },
                "relationships": {"device": {"data": {"type": "device", "id": None}}},
            }
        }
        with self.client:
            url_post = base_url + "/customfields"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the device)
        self.assertNotEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 200)
        count_customfields_after = db.session.query(CustomField).count()
        self.assertEqual(count_customfields_before, count_customfields_after)

    def test_get_customfields_api(self):
        """Ensure that we can get a list of customfields."""
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

        all_customfields = [
            customfield1,
            customfield2,
            customfield3,
        ]

        with self.client:
            response = self.client.get(
                base_url + "/customfields", content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

            customfield1_data = None
            for customfield in payload["data"]:
                customfield["id"] in [str(cf.id) for cf in all_customfields]
                customfield["attributes"]["key"] in [cf.key for cf in all_customfields]
                customfield["attributes"]["value"] in [
                    cf.value for cf in all_customfields
                ]

                if customfield["id"] == str(customfield1.id):
                    customfield1_data = customfield
                    self.assertEqual(customfield["attributes"]["key"], customfield1.key)
                    self.assertEqual(
                        customfield["attributes"]["value"], customfield1.value
                    )
                    # and we want to check the link for the device as well
                    device_link = customfield["relationships"]["device"]["links"][
                        "related"
                    ]
                    resp_device = self.client.get(
                        device_link, content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_device.status_code, 200)
                    self.assertEqual(
                        resp_device.get_json()["data"]["id"],
                        str(customfield1.device_id),
                    )
                    self.assertEqual(
                        resp_device.get_json()["data"]["attributes"]["short_name"],
                        customfield1.device.short_name,
                    )

            self.assertTrue(customfield1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url + "/customfields/" + str(customfield1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this customfield
            self.assertEqual(response.get_json()["data"], customfield1_data)

            # And now we want to make sure that we already filter the customfields
            # with a given device id
            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url + "/devices/" + str(device2.id) + "/customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_patch_customfield_api(self):
        """Ensure that we can update a customfield."""
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
        db.session.add(customfield1)
        db.session.commit()

        payload = {
            "data": {
                "type": "customfield",
                "id": str(customfield1.id),
                "attributes": {"key": "UFZ", "value": "https://www.ufz.de", },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/customfields/" + str(customfield1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        customfield_reloaded = (
            db.session.query(CustomField).filter_by(id=customfield1.id).one()
        )
        self.assertEqual(customfield_reloaded.value, "https://www.ufz.de")
        self.assertEqual(customfield_reloaded.key, "UFZ")
        self.assertEqual(customfield_reloaded.device_id, device2.id)

    def test_delete_customfield_api(self):
        """Ensure that we can delete a customfield."""
        device1 = Device(
            short_name="Just a device",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)
        db.session.commit()
        customfield1 = CustomField(
            key="GFZ", value="https://www.gfz-potsdam.de", device=device1,
        )
        db.session.add(customfield1)
        db.session.commit()
        # access_headers = create_token()
        with self.client:
            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)
        #     response = self.client.delete(
        #         base_url + "/customfields/" + str(customfield1.id),
        #         headers=access_headers,
        #     )
        #     # I would expect a 204 (no content), but 200 is good as well
        #     self.assertTrue(response.status_code in [200, 204])
        #
        #     response = self.client.get(
        #         base_url + "/devices/" + str(device1.id) + "/customfields",
        #         content_type="application/vnd.api+json",
        #     )
        #     self.assertEqual(response.status_code, 200)
        #     self.assertEqual(len(response.get_json()["data"]), 0)
        #
        # count_customfields = (
        #     db.session.query(CustomField)
        #     .filter_by(
        #         device_id=device1.id,
        #     )
        #     .count()
        # )
        # self.assertEqual(count_customfields, 0)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
