"""Tests for the device property endpoints."""

import json

from project import base_url
from project.api.models.base_model import db
from project.api.models.device import Device
from project.api.models.device_property import DeviceProperty
from project.tests.base import BaseTestCase, query_result_to_list
from project.tests.base import fake


class TestDevicePropertyServices(BaseTestCase):
    """Test device properties."""

    url = base_url + "/device-properties"

    def test_post_device_property_api(self):
        """Ensure that we can add a device property."""
        # First we need to make sure that we have a device
        device = Device(short_name="Very new device",)
        db.session.add(device)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(device.id is not None)

        count_device_properties = (
            db.session.query(DeviceProperty).filter_by(device_id=device.id,).count()
        )
        # However, this new device for sure has no properties
        self.assertEqual(count_device_properties, 0)

        # Now we can write the request to add a device property
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/device-properties"
            # You may want to look up self.add_object in the BaseTestCase
            # and compare if something doesn't work anymore
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        # We expect that it worked and that we have a new entry
        self.assertEqual(response.status_code, 201)
        # And we want to inspect our property list
        device_properties = query_result_to_list(
            db.session.query(DeviceProperty).filter_by(device_id=device.id,)
        )
        # We now have one property
        self.assertEqual(len(device_properties), 1)

        # And it is as we specified it
        device_property = device_properties[0]
        self.assertEqual(device_property.label, "device property1")
        self.assertEqual(device_property.compartment_name, "climate")
        self.assertEqual(device_property.sampling_media_name, "air")
        self.assertEqual(device_property.device_id, device.id)
        self.assertEqual(
            str(device_property.device_id), response.get_json()["data"]["id"]
        )

    def test_post_device_property_api_missing_device(self):
        """Ensure that we don't add a device property with missing device."""
        count_device_properties_before = db.session.query(DeviceProperty).count()
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {"label": "device property1",},
                "relationships": {"device": {"data": {"type": "device", "id": None}}},
            }
        }
        with self.client:
            url_post = base_url + "/device-properties"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        # it will not work, as we miss an important part (the device)
        self.assertEqual(response.status_code, 422)
        count_device_properties_after = db.session.query(DeviceProperty).count()
        self.assertEqual(count_device_properties_before, count_device_properties_after)

    def test_get_device_property_api(self):
        """Ensure that we can get a list of device properties."""
        device1 = Device(short_name="Just a device")
        device2 = Device(short_name="Another device")

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        device_property1 = DeviceProperty(label="device property1", device=device1,)
        device_property2 = DeviceProperty(label="device property2", device=device1,)
        device_property3 = DeviceProperty(label="device property3", device=device2,)

        db.session.add(device_property1)
        db.session.add(device_property2)
        db.session.add(device_property3)
        db.session.commit()

        all_device_properties = [
            device_property1,
            device_property2,
            device_property3,
        ]

        with self.client:
            response = self.client.get(
                base_url + "/device-properties",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

            device_property1_data = None
            for property in payload["data"]:
                property["id"] in [str(dp.id) for dp in all_device_properties]
                property["attributes"]["label"] in [
                    dp.label for dp in all_device_properties
                ]

                if property["id"] == str(device_property1.id):
                    device_property1_data = property
                    self.assertEqual(
                        property["attributes"]["label"], device_property1.label
                    )
                    # and we want to check the link for the device as well
                    device_link = property["relationships"]["device"]["links"][
                        "related"
                    ]
                    resp_device = self.client.get(
                        device_link, content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_device.status_code, 200)
                    self.assertEqual(
                        resp_device.get_json()["data"]["id"],
                        str(device_property1.device_id),
                    )
                    self.assertEqual(
                        resp_device.get_json()["data"]["attributes"]["short_name"],
                        device_property1.device.short_name,
                    )

            self.assertTrue(device_property1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url + "/device-properties/" + str(device_property1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this property
            self.assertEqual(response.get_json()["data"], device_property1_data)

            # And now we want to make sure that we already filter the device properties
            # with a given device id
            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/device-properties",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url + "/devices/" + str(device2.id) + "/device-properties",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_patch_device_property_api(self):
        """Ensure that we can update a device property."""
        device1 = Device(short_name="Just a device")
        device2 = Device(short_name="Another device")

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        device_property1 = DeviceProperty(label="property 1", device=device1,)
        db.session.add(device_property1)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {"label": "property 2",},
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/device-properties/" + str(device_property1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 200)

        device_property_reloaded = (
            db.session.query(DeviceProperty).filter_by(id=device_property1.id).one()
        )
        self.assertEqual(device_property_reloaded.label, "property 2")
        self.assertEqual(device_property_reloaded.device_id, device2.id)

    def test_delete_device_property_api(self):
        """Ensure that we can delete a device property."""
        device1 = Device(short_name="Just a device")
        db.session.add(device1)
        db.session.commit()
        device_property1 = DeviceProperty(label="property 1", device=device1,)
        db.session.add(device_property1)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/device-properties",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

            response = self.client.delete(
                base_url + "/device-properties/" + str(device_property1.id),
            )

            # I would expect a 204 (no content), but 200 is good as well
            self.assertTrue(response.status_code in [200, 204])

            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/device-properties",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 0)

        count_device_properties = (
            db.session.query(DeviceProperty).filter_by(device_id=device1.id,).count()
        )
        self.assertEqual(count_device_properties, 0)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
