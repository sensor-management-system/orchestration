# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the device property endpoints."""

import datetime
import json
import time
from unittest.mock import patch

import pytz
from flask import current_app

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationDynamicLocationBeginAction,
    Contact,
    DatastreamLink,
    Device,
    DeviceCalibrationAction,
    DeviceMountAction,
    DeviceProperty,
    DevicePropertyCalibration,
    TsmEndpoint,
    User,
)
from project.api.models.base_model import db
from project.extensions.instances import pidinst
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list


class TestDevicePropertyServices(BaseTestCase):
    """Test device properties."""

    url = base_url + "/device-properties"

    def test_post_device_property_api(self):
        """Ensure that we can add a device property."""
        # First we need to make sure that we have a device
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(device.id is not None)

        count_device_properties = (
            db.session.query(DeviceProperty)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        # However, this new device for sure has no properties
        self.assertEqual(count_device_properties, 0)

        # Now we can write the request to add a device property
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device_property1",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                    "aggregation_type_name": "Average",
                    "aggregation_type_uri": "https://sensors.gfz-potsdam.de/cv/api/v1/aggregationtypes/1/",
                    "accuracy_unit_name": "%",
                    "accuracy_unit_uri": "https://sensors.gfz-potsdam.de/cv/api/v1/units/1",
                    "description": "a test device property",
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
                headers=create_token(),
            )
        # We expect that it worked and that we have a new entry
        self.assertEqual(response.status_code, 201)
        # And we want to inspect our property list
        device_properties = query_result_to_list(
            db.session.query(DeviceProperty).filter_by(
                device_id=device.id,
            )
        )
        # We now have one property
        self.assertEqual(len(device_properties), 1)

        # And it is as we specified it
        device_property = device_properties[0]
        self.assertEqual(device_property.label, "device property1")
        self.assertEqual(device_property.compartment_name, "climate")
        self.assertEqual(device_property.sampling_media_name, "air")
        self.assertEqual(device_property.aggregation_type_name, "Average")
        self.assertEqual(
            device_property.aggregation_type_uri,
            "https://sensors.gfz-potsdam.de/cv/api/v1/aggregationtypes/1/",
        )
        self.assertEqual(device_property.accuracy_unit_name, "%")
        self.assertEqual(
            device_property.accuracy_unit_uri,
            "https://sensors.gfz-potsdam.de/cv/api/v1/units/1",
        )
        self.assertEqual(device_property.description, "a test device property")
        self.assertEqual(device_property.device_id, device.id)
        self.assertEqual(
            str(device_property.device_id), response.get_json()["data"]["id"]
        )
        msg = "create;measured quantity"
        self.assertEqual(msg, device_property.device.update_description)

    def test_post_device_property_api_missing_device(self):
        """Ensure that we don't add a device property with missing device."""
        count_device_properties_before = db.session.query(DeviceProperty).count()
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device_property1",
                },
                "relationships": {"device": {"data": {"type": "device", "id": None}}},
            }
        }
        with self.client:
            url_post = base_url + "/device-properties"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the device)
        self.assertNotEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 200)
        count_device_properties_after = db.session.query(DeviceProperty).count()
        self.assertEqual(count_device_properties_before, count_device_properties_after)

    def test_get_device_property_api(self):
        """Ensure that we can get a list of device properties."""
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
            short_name="Another device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        device_property1 = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            description="Device property 1",
            accuracy_unit_name="%",
            accuracy_unit_uri="https://sensors.gfz-potsdam.de/cv/api/v1/units/1",
            device=device1,
        )
        device_property2 = DeviceProperty(
            label="device property2",
            property_name="device_property2",
            device=device1,
        )
        device_property3 = DeviceProperty(
            label="device property3",
            property_name="device_property3",
            device=device2,
        )

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
                    self.assertEqual(
                        property["attributes"]["description"],
                        device_property1.description,
                    )
                    self.assertEqual(
                        property["attributes"]["accuracy_unit_name"],
                        device_property1.accuracy_unit_name,
                    )
                    self.assertEqual(
                        property["attributes"]["accuracy_unit_uri"],
                        device_property1.accuracy_unit_uri,
                    )
                    # and we want to check the link for the device as well
                    device_link = property["relationships"]["device"]["links"][
                        "related"
                    ]
                    resp_device = self.client.get(
                        device_link,
                        content_type="application/vnd.api+json",
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
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        device2 = Device(
            short_name="Another device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device1,
        )
        db.session.add(device_property1)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {
                    "label": "property 2",
                    "property_name": "device_property2",
                },
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
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        device_property_reloaded = (
            db.session.query(DeviceProperty).filter_by(id=device_property1.id).one()
        )
        self.assertEqual(device_property_reloaded.label, "property 2")
        self.assertEqual(device_property_reloaded.device_id, device2.id)
        msg = "update;measured quantity"
        self.assertEqual(msg, device_property_reloaded.device.update_description)

    def test_delete_device_property_api(self):
        """Ensure that we can delete a device property."""
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)
        db.session.commit()
        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device1,
        )
        db.session.add(device_property1)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/device-properties",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

        #     response = self.client.delete(
        #         base_url + "/device-properties/" + str(device_property1.id),
        #         headers=create_token(),
        #     )
        #
        #     # I would expect a 204 (no content), but 200 is good as well
        #     self.assertTrue(response.status_code in [200, 204])
        #
        #     response = self.client.get(
        #         base_url + "/devices/" + str(device1.id) + "/device-properties",
        #         content_type="application/vnd.api+json",
        #     )
        #     self.assertEqual(response.status_code, 200)
        #     self.assertEqual(len(response.get_json()["data"]), 0)
        #
        # count_device_properties = (
        #     db.session.query(DeviceProperty)
        #     .filter_by(
        #         device_id=device1.id,
        #     )
        #     .count()
        # )
        # self.assertEqual(count_device_properties, 0)
        access_headers = create_token()
        with self.client:
            response = self.client.delete(
                base_url + "/devices/" + str(device1.id) + "/device-properties",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertNotEqual(response.status_code, 200)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_post_without_mandatory_fields(self):
        """Make sure that a request will fail if property_name is None."""
        device = Device(
            short_name="New device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()
        self.assertTrue(device.id is not None)

        count_device_properties = (
            db.session.query(DeviceProperty)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        self.assertEqual(count_device_properties, 0)

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
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertNotEqual(response.status_code, 201)

    def test_created_and_updated_fields(self):
        """Ensure we set & update the created & updated metainformation."""
        contact1 = Contact(
            given_name="first", family_name="contact", email="first@contact.org"
        )
        contact2 = Contact(
            given_name="second", family_name="contact", email="second@contact.org"
        )
        user1 = User(contact=contact1, subject=contact1.email, is_superuser=True)
        user2 = User(contact=contact2, subject=contact2.email, is_superuser=True)
        device1 = Device(short_name="dummy device", is_public=True)

        db.session.add_all([contact1, contact2, user1, user2, device1])
        db.session.commit()

        with self.run_requests_as(user1):
            response1 = self.client.post(
                self.url,
                data=json.dumps(
                    {
                        "data": {
                            "type": "device_property",
                            "attributes": {
                                "property_name": "Air temperature",
                                "label": "Temp",
                            },
                            "relationships": {
                                "device": {"data": {"type": "device", "id": device1.id}}
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response1.status_code, 201)
        property_id = response1.json["data"]["id"]

        one_second = 1
        time.sleep(one_second)

        with self.run_requests_as(user2):
            response2 = self.client.patch(
                f"{self.url}/{property_id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device_property",
                            "id": property_id,
                            "attributes": {
                                "label": "Temperature",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(
            response1.json["data"]["attributes"]["created_at"],
            response2.json["data"]["attributes"]["created_at"],
        )

        self.assertEqual(
            response1.json["data"]["relationships"]["created_by"]["data"]["id"],
            response2.json["data"]["relationships"]["created_by"]["data"]["id"],
        )
        self.assertEqual(
            response1.json["data"]["relationships"]["created_by"]["data"]["id"],
            str(user1.id),
        )

        self.assertEqual(
            response2.json["data"]["relationships"]["updated_by"]["data"]["id"],
            str(user2.id),
        )

        self.assertTrue(
            # Due to the iso format it is enought to compare them as stirngs
            # here, as 2023-03-14T12:00:00 is < then 2023-03-14T12:00:01.
            response1.json["data"]["attributes"]["updated_at"]
            < response2.json["data"]["attributes"]["updated_at"]
        )


class TestDevicePropertyDeletion(BaseTestCase):
    """Test class for deleting with some relationships."""

    url = base_url + "/device-properties"

    def setUp(self):
        """Set some test data up."""
        super().setUp()
        self.device = Device(
            short_name="Very new device",
            manufacturer_name="Some company",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        self.device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=self.device,
        )
        self.contact = Contact(
            given_name="first", family_name="contact", email="first@contact.org"
        )
        self.super_user = User(
            contact=self.contact, subject=self.contact.email, is_superuser=True
        )
        db.session.add_all(
            [self.device, self.device_property, self.contact, self.super_user]
        )
        db.session.commit()

    def test_delete_with_existing_datastream_link(self):
        """Ensure we can't delete if there is a datastream link pointing to the property."""
        configuration = Configuration(
            label="config1",
            is_internal=True,
            is_public=False,
            cfg_permission_group="1",
        )
        device_mount = DeviceMountAction(
            configuration=configuration,
            device=self.device,
            begin_contact=self.contact,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.utc),
            end_date=datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc),
        )
        tsm_endpoint = TsmEndpoint(url="https://somewhere", name="Somewhere")
        datastream_link = DatastreamLink(
            device_mount_action=device_mount,
            device_property=self.device_property,
            tsm_endpoint=tsm_endpoint,
            datasource_id="1",
            datasource_name="1",
            thing_id="2",
            thing_name="2",
            datastream_id="3",
            datastream_name="3",
            begin_date=device_mount.begin_date,
            end_date=device_mount.end_date,
        )
        db.session.add_all([configuration, device_mount, tsm_endpoint, datastream_link])
        db.session.commit()

        with self.run_requests_as(self.super_user):
            resp = self.client.delete(f"{self.url}/{self.device_property.id}")
        self.assertEqual(resp.status_code, 409)

    def test_delete_with_existing_dynamic_location(self):
        """Ensure we can't delete if there is a dynamic location pointing to the property."""
        configuration = Configuration(
            label="config1",
            is_internal=True,
            is_public=False,
            cfg_permission_group="1",
        )
        device_mount = DeviceMountAction(
            configuration=configuration,
            device=self.device,
            begin_contact=self.contact,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0, tzinfo=pytz.utc),
            end_date=datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc),
        )
        location = ConfigurationDynamicLocationBeginAction(
            configuration=configuration,
            x_property=self.device_property,
            y_property=self.device_property,
            z_property=self.device_property,
            begin_date=device_mount.begin_date,
            end_date=device_mount.end_date,
            begin_contact=self.contact,
        )
        db.session.add_all([configuration, device_mount, location])
        with self.run_requests_as(self.super_user):
            resp = self.client.delete(f"{self.url}/{self.device_property.id}")
        self.assertEqual(resp.status_code, 409)

    def test_delete_with_existing_calibration(self):
        """Ensure we can't delete if there is a calibration action pointing to the property."""
        calibration = DeviceCalibrationAction(
            device=self.device,
            contact=self.contact,
            current_calibration_date=datetime.datetime(
                2022, 1, 1, 12, 0, 0, tzinfo=pytz.utc
            ),
        )
        property_calibration = DevicePropertyCalibration(
            calibration_action=calibration,
            device_property=self.device_property,
        )
        db.session.add_all([calibration, property_calibration])
        with self.run_requests_as(self.super_user):
            resp = self.client.delete(f"{self.url}/{self.device_property.id}")
        self.assertEqual(resp.status_code, 409)

    def test_update_external_metadata_post_device_property(self):
        """Ensure we ask the system to update external metadata after posting a device property."""
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
            b2inst_record_id="42",
        )
        db.session.add(device)
        db.session.commit()

        # Now we can write the request to add a device property
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device_property1",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                    "aggregation_type_name": "Average",
                    "aggregation_type_uri": "https://sensors.gfz-potsdam.de/cv/api/v1/aggregationtypes/1/",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        url_post = base_url + "/device-properties"
        with self.client:

            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                self.client.post(
                    url_post,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, device.id
                )

    def test_update_external_metadata_patch_device_property(self):
        """Ensure we ask the system to update external metadata after patching a device property."""
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
            b2inst_record_id="42",
        )

        db.session.add(device1)
        db.session.commit()

        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device1,
        )
        db.session.add(device_property1)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {
                    "label": "property 2",
                    "property_name": "device_property2",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device1.id)}}
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        url_patch = base_url + "/device-properties/" + str(device_property1.id)
        with self.client:

            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                self.client.patch(
                    url_patch,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, device1.id
                )

    def test_update_external_metadata_delete_device_property(self):
        """Ensure we ask the system to update external metadata after deleting a device property."""
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
            b2inst_record_id="42",
        )
        db.session.add(device1)
        db.session.commit()
        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device1,
        )
        db.session.add(device_property1)
        db.session.commit()

        access_headers = create_token()
        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.client:
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                self.client.delete(
                    base_url + "/device-properties/" + str(device_property1.id),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, device1.id
                )

    def test_update_external_metadata_for_configuration_post_device_property(self):
        """Ensure to update pidinst for the configuration after posting device property."""
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        configuration = Configuration(label="test config", b2inst_record_id="42")
        contact = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        device_mount_action = DeviceMountAction(
            device=device,
            begin_contact=contact,
            configuration=configuration,
            offset_x=0,
            offset_y=0,
            offset_z=0,
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        )

        db.session.add_all([device, configuration, contact, device_mount_action])
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device_property1",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                    "aggregation_type_name": "Average",
                    "aggregation_type_uri": "https://sensors.gfz-potsdam.de/cv/api/v1/aggregationtypes/1/",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        url_post = base_url + "/device-properties"
        with self.client:

            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                self.client.post(
                    url_post,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, configuration.id
                )

    def test_update_external_metadata_for_configuration_patch_device_property(self):
        """Ensure to update pidinst for the configuration after patching device property."""
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        configuration = Configuration(label="test config", b2inst_record_id="42")
        contact = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        device_mount_action = DeviceMountAction(
            device=device,
            begin_contact=contact,
            configuration=configuration,
            offset_x=0,
            offset_y=0,
            offset_z=0,
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        )

        db.session.add_all([device, configuration, contact, device_mount_action])
        db.session.commit()

        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device,
        )
        db.session.add(device_property1)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_property",
                "id": str(device_property1.id),
                "attributes": {
                    "label": "property 2",
                    "property_name": "device_property2",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        url_patch = base_url + "/device-properties/" + str(device_property1.id)
        with self.client:

            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                self.client.patch(
                    url_patch,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, configuration.id
                )

    def test_update_external_metadata_for_configuration_delete_device_property(self):
        """Ensure to update pidinst for the configuration after deleting a device property."""
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        configuration = Configuration(label="test config", b2inst_record_id="42")
        contact = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        device_mount_action = DeviceMountAction(
            device=device,
            begin_contact=contact,
            configuration=configuration,
            offset_x=0,
            offset_y=0,
            offset_z=0,
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        )

        db.session.add_all([device, configuration, contact, device_mount_action])
        db.session.commit()
        device_property1 = DeviceProperty(
            label="property 1",
            property_name="device_property1",
            device=device,
        )
        db.session.add(device_property1)
        db.session.commit()

        access_headers = create_token()
        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.client:
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                self.client.delete(
                    base_url + "/device-properties/" + str(device_property1.id),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, configuration.id
                )
