# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the device property calibration api."""
from project import base_url
from project.api.models import (
    Contact,
    Device,
    DeviceCalibrationAction,
    DeviceProperty,
    DevicePropertyCalibration,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.models.test_device_calibration_action_model import (
    add_device_property_calibration_model,
)


class TestDevicePropertyCalibration(BaseTestCase):
    """Tests for the DevicePropertyCalibration endpoints."""

    url = base_url + "/device-property-calibrations"
    object_type = "device_property_calibration"

    def test_get_device_property_calibration(self):
        """Ensure the GET /device_property_calibration route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_property_calibration_collection(self):
        """Test retrieve a collection of DevicePropertyCalibration objects."""
        device_property_calibration_model = add_device_property_calibration_model()
        device = device_property_calibration_model.calibration_action.device
        device.is_public = True
        device.is_internal = False
        db.session.add(device)
        db.session.commit()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"], str(device_property_calibration_model.id)
        )

    def test_post_device_property_calibration(self):
        """Create DevicePropertyCalibration."""
        device = Device(
            short_name="Device 200",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device_property = DeviceProperty(
            device=device,
            measuring_range_min=fake.pyfloat(),
            measuring_range_max=fake.pyfloat(),
            failure_value=fake.pyfloat(),
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            compartment_uri=fake.uri(),
            compartment_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test property_name",
            sampling_media_uri=fake.uri(),
            sampling_media_name=fake.pystr(),
        )
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        device_calibration_action = DeviceCalibrationAction(
            description="Test DeviceCalibrationAction",
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add_all(
            [device, contact, device_property, device_calibration_action]
        )
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "device_property": {
                        "data": {"type": "device_property", "id": device_property.id}
                    },
                    "calibration_action": {
                        "data": {
                            "type": "device_calibration_action",
                            "id": device_calibration_action.id,
                        }
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=device_property,calibration_action",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_device_property_calibration(self):
        """Update DevicePropertyCalibration."""
        userinfo = generate_userinfo_data()
        device = Device(
            short_name="Device 300",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )

        device_calibration_action = DeviceCalibrationAction(
            description="Test DeviceCalibrationAction",
            formula=fake.pystr(),
            value=fake.pyfloat(),
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact,
        )
        db.session.add_all([device, contact, device_calibration_action])
        db.session.commit()
        dpa = add_device_property_calibration_model()
        data = {
            "data": {
                "type": self.object_type,
                "id": dpa.id,
                "attributes": {},
                "relationships": {
                    "calibration_action": {
                        "data": {
                            "type": "device_calibration_action",
                            "id": device_calibration_action.id,
                        }
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{dpa.id}?include=calibration_action",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_device_property_calibration(self):
        """Delete DevicePropertyCalibration."""
        device_property_calibration = add_device_property_calibration_model()
        _ = super().delete_object(
            url=f"{self.url}/{device_property_calibration.id}",
        )

    def _create_some_device_property_calibrations(self):
        """Create some devices, properties, & device property calibrations."""
        device1 = Device(
            short_name="sample device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)
        device2 = Device(
            short_name="sample device II",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        device_property1 = DeviceProperty(
            device=device1,
            label="prop1",
            property_name="device_property1",
        )
        db.session.add(device_property1)

        device_property2 = DeviceProperty(
            device=device1,
            label="prop2",
            property_name="device_property2",
        )
        db.session.add(device_property2)

        device_property3 = DeviceProperty(
            device=device2,
            label="prop3",
            property_name="device_property3",
        )
        db.session.add(device_property3)

        device_property4 = DeviceProperty(
            device=device2,
            label="prop4",
            property_name="device_property4",
        )
        db.session.add(device_property4)

        contact1 = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact1)

        contact2 = Contact(given_name="max", family_name="Mustermann", email="mx@mu.mn")

        action1 = DeviceCalibrationAction(
            device=device1,
            contact=contact1,
            description="Some first action",
            current_calibration_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceCalibrationAction(
            device=device2,
            contact=contact2,
            description="Some other action",
            current_calibration_date=fake.date_time(),
        )
        db.session.add(action2)

        device_property_calibration1 = DevicePropertyCalibration(
            device_property=device_property1,
            calibration_action=action1,
        )
        db.session.add(device_property1)

        device_property_calibration2 = DevicePropertyCalibration(
            device_property=device_property2,
            calibration_action=action1,
        )
        db.session.add(device_property2)

        device_property_calibration3 = DevicePropertyCalibration(
            device_property=device_property3,
            calibration_action=action2,
        )
        db.session.add(device_property3)
        device_property_calibration4 = DevicePropertyCalibration(
            device_property=device_property4,
            calibration_action=action2,
        )
        db.session.add(device_property2)

        db.session.commit()

        return {
            "device_calibration_action_ids": [action1.id, action2.id],
            "device_ids": [device1.id, device2.id],
            "device_property_ids": [
                device_property1.id,
                device_property2.id,
                device_property3.id,
                device_property4.id,
            ],
            "device_property_calibration_ids": [
                device_property_calibration1.id,
                device_property_calibration2.id,
                device_property_calibration3.id,
                device_property_calibration4.id,
            ],
            "contact_ids": [contact1.id, contact2.id],
        }

    def test_filtered_by_device_calibration_action(self):
        """Ensure that I can prefilter by a specific device calibration action."""
        data = self._create_some_device_property_calibrations()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/device-property-calibrations"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 4)

        # then test only for the first action
        action1_id = data["device_calibration_action_ids"][0]
        with self.client:
            url_get_for_action1 = (
                base_url
                + f"/device-calibration-actions/{action1_id}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_action1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)
        self.assertIn(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][:2]],
        )
        self.assertIn(
            response.json["data"][1]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][:2]],
        )

        # and test the second action
        action2_id = data["device_calibration_action_ids"][1]
        with self.client:
            url_get_for_action2 = (
                base_url
                + f"/device-calibration-actions/{action2_id}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_action2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)
        self.assertIn(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][2:]],
        )
        self.assertIn(
            response.json["data"][1]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][2:]],
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url
                + f"/device-calibration-actions/{action2_id + 9999}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_device_calibration_action_id(self):
        """Ensure that I can prefilter by filter[calibration_action_id]."""
        data = self._create_some_device_property_calibrations()

        # Test only for the first action
        action1_id = data["device_calibration_action_ids"][0]
        with self.client:
            url_get_for_action1 = (
                base_url
                + f"/device-property-calibrations?filter[calibration_action_id]={action1_id}"
            )
            response = self.client.get(
                url_get_for_action1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)
        self.assertIn(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][:2]],
        )
        self.assertIn(
            response.json["data"][1]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][:2]],
        )

        # and test the second action
        action2_id = data["device_calibration_action_ids"][1]
        with self.client:
            url_get_for_action2 = (
                base_url
                + f"/device-property-calibrations?filter[calibration_action_id]={action2_id}"
            )
            response = self.client.get(
                url_get_for_action2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)
        self.assertIn(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][2:]],
        )
        self.assertIn(
            response.json["data"][1]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][2:]],
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url
                + f"/device-property-calibrations?filter[calibration_action_id]={action2_id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_filtered_by_device_property(self):
        """Ensure that I can prefilter by a specific device property."""
        data = self._create_some_device_property_calibrations()

        # test only for the first device property
        device_property1_id = data["device_property_ids"][0]
        with self.client:
            url_get_for_device_property1 = (
                base_url
                + f"/device-properties/{device_property1_id}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_device_property1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            str(device_property1_id),
        )

        # and test the second device property
        device_property2_id = data["device_property_ids"][1]
        with self.client:
            url_get_for_device_property2 = (
                base_url
                + f"/device-properties/{device_property2_id}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_device_property2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            str(device_property2_id),
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url
                + f"/device-properties/{device_property2_id + 9999}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_device_property_id(self):
        """Ensure that I can prefilter by filter[device_property_id]."""
        data = self._create_some_device_property_calibrations()

        # Test only for the first device property
        device_property1_id = data["device_property_ids"][0]
        with self.client:
            url_get_for_device_property1 = (
                base_url
                + f"/device-property-calibrations?filter[device_property_id]={device_property1_id}"
            )
            response = self.client.get(
                url_get_for_device_property1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            str(device_property1_id),
        )

        # and test the second device property
        device_property2_id = data["device_property_ids"][1]
        with self.client:
            url_get_for_device_property2 = (
                base_url
                + f"/device-property-calibrations?filter[device_property_id]={device_property2_id}"
            )
            response = self.client.get(
                url_get_for_device_property2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            str(device_property2_id),
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url
                + f"/device-property-calibrations?filter[device_property_id]={device_property2_id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_filtered_by_device(self):
        """Ensure that I can prefilter by a specific device."""
        data = self._create_some_device_property_calibrations()

        # then test only for the first device
        device1_id = data["device_ids"][0]
        with self.client:
            url_get_for_device1 = (
                base_url + f"/devices/{device1_id}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_device1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)
        self.assertIn(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][:2]],
        )
        self.assertIn(
            response.json["data"][1]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][:2]],
        )

        # and test the second device
        device2_id = data["device_ids"][1]
        with self.client:
            url_get_for_device2 = (
                base_url + f"/devices/{device2_id}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_device2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)
        self.assertIn(
            response.json["data"][0]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][2:]],
        )
        self.assertIn(
            response.json["data"][1]["relationships"]["device_property"]["data"]["id"],
            [str(x) for x in data["device_property_ids"][2:]],
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url + f"/devices/{device2_id + 9999}/device-property-calibrations"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 404)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
