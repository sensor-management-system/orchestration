import datetime
import json
import os

from project import base_url
from project.api.models import Contact
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.configuration_device import ConfigurationDevice
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.tests.base import BaseTestCase, create_token, test_file_path
from project.tests.base import fake, generate_token_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.read_from_json import extract_data_from_json_file


class TestConfigurationsService(BaseTestCase):
    """Tests for the Configurations Service."""

    configurations_url = base_url + "/configurations"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    object_type = "configuration"
    json_data_url = os.path.join(
        test_file_path, "drafts", "configurations_test_data.json"
    )
    device_json_data_url = os.path.join(
        test_file_path, "drafts", "devices_test_data.json"
    )
    platform_json_data_url = os.path.join(
        test_file_path, "drafts", "platforms_test_data.json"
    )
    device_mount_url = base_url + "/device-mount-actions"
    platform_mount_url = base_url + "/platform-mount-actions"

    def test_get_configurations(self):
        """Ensure the GET /configurations route behaves correctly."""
        response = self.client.get(self.configurations_url)
        self.assertEqual(response.status_code, 200)
        # There are no data sets inserted yet.
        self.assertEqual(response.json["data"], [])

    def test_add_configuration(self):
        """Ensure POST a new configuration can be added to the database."""

        # we want to run the very same test with multiple dates
        calibration_dates = {
            "20201111": {
                "json_api_value": "2020-11-11T00:00:00",
                "sql_alchemy_value": datetime.datetime(
                    year=2020, month=11, day=11, hour=0, minute=0, second=0
                ),
            },
            "20200229": {
                "json_api_value": "2020-02-29T00:00:00",
                "sql_alchemy_value": datetime.datetime(
                    year=2020, month=2, day=29, hour=0, minute=0, second=0
                ),
            },
            "2020-08-29T13:49:48.015620+00:00": {
                "json_api_value": "2020-08-29T13:49:48.015620",
                # first this should be wrong
                "sql_alchemy_value": datetime.datetime(
                    year=2020,
                    month=8,
                    day=29,
                    hour=13,
                    minute=49,
                    second=48,
                    microsecond=15620,
                ),
            },
        }
        for (
            input_calibration_date,
            expected_output_calibration_date,
        ) in calibration_dates.items():
            # set up for each single run
            self.setUp()

            devices_json = extract_data_from_json_file(
                self.device_json_data_url, "devices"
            )

            device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
            super().add_object(
                url=self.device_url, data_object=device_data, object_type="device"
            )

            platforms_json = extract_data_from_json_file(
                self.platform_json_data_url, "platforms"
            )

            platform_data = {
                "data": {"type": "platform", "attributes": platforms_json[0]}
            }

            super().add_object(
                url=self.platform_url, data_object=platform_data, object_type="platform"
            )

            config_json = extract_data_from_json_file(
                self.json_data_url, "configuration"
            )

            config_json[0]["hierarchy"][0]["children"][0][
                "calibration_date"
            ] = input_calibration_date

            config_data = {
                "data": {"type": "configuration", "attributes": config_json[0]}
            }
            res = super().add_object(
                url=self.configurations_url,
                data_object=config_data,
                object_type=self.object_type,
            )
            self.assertEqual(
                expected_output_calibration_date["json_api_value"],
                res["data"]["attributes"]["hierarchy"][0]["children"][0][
                    "calibration_date"
                ],
            )

            configuration_device = (
                db.session.query(ConfigurationDevice)
                .filter_by(device_id=1, configuration_id=1)
                .first()
            )
            self.assertEqual(
                configuration_device.calibration_date,
                expected_output_calibration_date["sql_alchemy_value"],
            )

            # clean up after each run
            self.tearDown()

    def test_add_configuration_with_firmware_version(self):
        """Ensure POST a new configuration (+ firmware) can be added to the database."""

        # we want to run the very same test with multiple dates
        firmware_version = "v.1.0"

        devices_json = extract_data_from_json_file(self.device_json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        super().add_object(
            url=self.device_url, data_object=device_data, object_type="device"
        )

        platforms_json = extract_data_from_json_file(
            self.platform_json_data_url, "platforms"
        )

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        super().add_object(
            url=self.platform_url, data_object=platform_data, object_type="platform"
        )

        config_json = extract_data_from_json_file(self.json_data_url, "configuration")

        config_json[0]["hierarchy"][0]["children"][0][
            "firmware_version"
        ] = firmware_version

        config_data = {"data": {"type": "configuration", "attributes": config_json[0]}}
        res = super().add_object(
            url=self.configurations_url,
            data_object=config_data,
            object_type=self.object_type,
        )
        self.assertEqual(
            firmware_version,
            res["data"]["attributes"]["hierarchy"][0]["children"][0][
                "firmware_version"
            ],
        )

        configuration_device = (
            db.session.query(ConfigurationDevice)
            .filter_by(device_id=1, configuration_id=1)
            .first()
        )
        self.assertEqual(configuration_device.firmware_version, firmware_version)

    def test_add_configuration_with_int_as_calibration_type(self):
        """Ensure That a Post for a new configuration
        with value-type for calibration-date = integer throw
        a type error."""

        devices_json = extract_data_from_json_file(self.device_json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        super().add_object(
            url=self.device_url, data_object=device_data, object_type="device"
        )

        platforms_json = extract_data_from_json_file(
            self.platform_json_data_url, "platforms"
        )

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        super().add_object(
            url=self.platform_url, data_object=platform_data, object_type="platform"
        )

        config_json = extract_data_from_json_file(self.json_data_url, "configuration")

        config_data = {"data": {"type": "configuration", "attributes": config_json[1]}}
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configurations_url,
                data=json.dumps(config_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)

    def test_add_configuration_with_false_string_as_calibration_type(self):
        """Ensure That a Post for a new configuration
        with false string value for calibration-date throw
        a type error."""

        devices_json = extract_data_from_json_file(self.device_json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        super().add_object(
            url=self.device_url, data_object=device_data, object_type="device"
        )

        platforms_json = extract_data_from_json_file(
            self.platform_json_data_url, "platforms"
        )

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        super().add_object(
            url=self.platform_url, data_object=platform_data, object_type="platform"
        )

        config_json = extract_data_from_json_file(self.json_data_url, "configuration")

        config_data = {"data": {"type": "configuration", "attributes": config_json[2]}}
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configurations_url,
                data=json.dumps(config_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)

    def test_support_include_devices_and_platforms_on_rest_call(self):
        """
        Ensure that we can ask to include devices & platforms.

        When we ask for a configuration via the rest interface,
        we also want to query the devices & platforms together
        within this call.
        """
        # add a configuration, the same way as
        # in test_add_configuration_model
        platform1 = Platform(short_name="Platform 1")
        platform2 = Platform(short_name="Platform 2")
        platform3 = Platform(short_name="Platform 3")

        db.session.add(platform1)
        db.session.add(platform2)
        db.session.add(platform3)

        device1 = Device(short_name="Device 1")
        device2 = Device(short_name="Device 2")
        device3 = Device(short_name="Device 3")

        db.session.add(device1)
        db.session.add(device2)
        db.session.add(device3)

        config1 = Configuration(label="Config1", location_type="static")
        db.session.add(config1)
        db.session.commit()

        platform1_conf = ConfigurationPlatform(
            platform=platform1,
            configuration=config1,
            offset_x=1.0,
            offset_y=1.0,
            offset_z=1.0,
        )
        db.session.add(platform1_conf)

        platform2_conf = ConfigurationPlatform(
            platform=platform2,
            configuration=config1,
            parent_platform=platform1,
            offset_x=2.0,
            offset_y=2.0,
            offset_z=2.0,
        )
        platform3_conf = ConfigurationPlatform(
            platform=platform3,
            configuration=config1,
            offset_x=13.5,
            offset_y=13.5,
            offset_z=13.5,
        )

        db.session.add(platform2_conf)
        db.session.add(platform3_conf)

        device1_conf = ConfigurationDevice(
            device=device1,
            configuration=config1,
            parent_platform=platform2,
            offset_x=0.5,
            offset_y=0.5,
            offset_z=0.5,
        )
        device2_conf = ConfigurationDevice(
            device=device2,
            configuration=config1,
            parent_platform=platform2,
            offset_x=0.6,
            offset_y=0.6,
            offset_z=0.6,
        )
        device3_conf = ConfigurationDevice(
            device=device3,
            configuration=config1,
            parent_platform=platform2,
            offset_x=0.65,
            offset_y=0.65,
            offset_z=0.65,
        )

        db.session.add(device1_conf)
        db.session.add(device2_conf)
        db.session.add(device3_conf)

        db.session.commit()

        with self.client:
            url = "".join(
                [
                    self.configurations_url,
                    "/",
                    str(config1.id),
                    "?",
                    "include",
                    "=",
                    ",".join(
                        [
                            "contacts",
                            "configuration_platforms.platform",
                            "configuration_devices.device",
                            "src_longitude",
                            "src_latitude",
                            "src_elevation",
                        ]
                    ),
                ]
            )
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            for key in ["data", "included"]:
                self.assertIn(key, response.json.keys())

            data = response.json["data"]
            self.assertNotEqual(data["attributes"]["hierarchy"], [])
            self.assertEqual(data["attributes"]["label"], config1.label)

            included = response.json["included"]

            self.assertTrue(len(included) >= 6)

            for device in [device1, device2, device3]:
                found = False
                for entry in included:
                    if entry["type"] == "device" and entry["id"] == str(device.id):
                        found = True
                        self.assertEqual(
                            entry["attributes"]["short_name"], device.short_name
                        )
                self.assertTrue(found)

            for platform in [platform1, platform2, platform3]:
                found = False
                for entry in included:
                    if entry["type"] == "platform" and entry["id"] == str(platform.id):
                        found = True
                        self.assertEqual(
                            entry["attributes"]["short_name"], platform.short_name
                        )
                self.assertTrue(found)

    def test_delete_configuration_which_still_contains_actions(self):
        """
        Ensure that we can delete a configuration and it's
        included actions.

        """
        device = Device(short_name=fake.linux_processor(),)
        device_parent_platform = Platform(short_name="device parent platform",)
        platform = Platform(short_name=fake.linux_processor(),)
        parent_platform = Platform(short_name="platform parent-platform",)
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        configuration = generate_configuration_model()
        db.session.add_all(
            [
                device,
                device_parent_platform,
                platform,
                parent_platform,
                contact,
                configuration,
            ]
        )
        db.session.commit()
        # Mount a device
        device_mount_data = {
            "data": {
                "type": "device_mount_action",
                "attributes": {
                    "description": "Test DeviceMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": device_parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.device_mount_url}?include=device,contact,parent_platform,configuration",
            data_object=device_mount_data,
            object_type="device_mount_action",
        )
        # Mount a Platform
        platform_mount_data = {
            "data": {
                "type": "platform_mount_action",
                "attributes": {
                    "description": "Test PlatformMountAction",
                    "begin_date": fake.future_datetime().__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": platform.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.platform_mount_url}?include=platform,contact,parent_platform,configuration",
            data_object=platform_mount_data,
            object_type="platform_mount_action",
        )

        _ = super().delete_object(url=f"{self.configurations_url}/{configuration.id}",)

    def test_delete_configuration_with_static_begin_location_action(self):
        """Ensure a configuration with a static_begin_location_action can be deleted"""
        contact = self.add_a_contact()
        config_id = self.add_a_configuration()

        action_data = {
            "data": {
                "type": "configuration_static_location_begin_action",
                "attributes": {
                    "x": 12.424163818359377,
                    "y": 51.40391771800119,
                    "z": None,
                    "description": "",
                    "begin_date": "2021-10-22T09:28:40.275Z",
                    "epsg_code": "4326",
                    "elevation_datum_uri": "",
                    "elevation_datum_name": "MSL",
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config_id}
                    },
                },
            }
        }
        url = base_url + "/static-location-begin-actions"
        _ = super().add_object(
            url=url,
            data_object=action_data,
            object_type="configuration_static_location_begin_action",
        )
        _ = super().delete_object(url=f"{self.configurations_url}/{config_id}",)

    def test_delete_configuration_with_static_end_location_action(self):
        """Ensure a configuration with a static_end_location_action can be deleted"""
        contact = self.add_a_contact()
        config_id = self.add_a_configuration()

        action_data = {
            "data": {
                "type": "configuration_static_location_end_action",
                "attributes": {
                    "description": "stopped",
                    "end_date": "2021-10-31T09:28:00.000Z",
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config_id}
                    },
                },
            }
        }
        url = base_url + "/static-location-end-actions"
        _ = super().add_object(
            url=url,
            data_object=action_data,
            object_type="configuration_static_location_end_action",
        )
        _ = super().delete_object(url=f"{self.configurations_url}/{config_id}",)

    def test_delete_configuration_with_dynamic_begin_location_action(self):
        """Ensure a configuration with a dynamic_begin_location_action can be deleted"""
        contact = self.add_a_contact()
        config_id = self.add_a_configuration()

        action_data = {
            "data": {
                "type": "configuration_dynamic_location_begin_action",
                "attributes": {
                    "description": "dynamic",
                    "begin_date": "2021-10-22T10:00:50.542Z",
                    "epsg_code": "4326",
                    "elevation_datum_uri": "",
                    "elevation_datum_name": "MSL",
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config_id}
                    },
                },
            }
        }
        url = base_url + "/dynamic-location-begin-actions"
        _ = super().add_object(
            url=url,
            data_object=action_data,
            object_type="configuration_dynamic_location_begin_action",
        )
        _ = super().delete_object(url=f"{self.configurations_url}/{config_id}",)

    def test_delete_configuration_with_dynamic_end_location_action(self):
        """Ensure a configuration with a dynamic_end_location_action can be deleted"""
        contact = self.add_a_contact()
        config_id = self.add_a_configuration()

        action_data = {
            "data": {
                "type": "configuration_dynamic_location_end_action",
                "attributes": {
                    "description": "Stopped",
                    "end_date": "2021-10-23T10:00:00.000Z",
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config_id}
                    },
                },
            }
        }
        url = base_url + "/dynamic-location-end-actions"
        _ = super().add_object(
            url=url,
            data_object=action_data,
            object_type="configuration_dynamic_location_end_action",
        )
        _ = super().delete_object(url=f"{self.configurations_url}/{config_id}",)

    @staticmethod
    def add_a_contact():
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )
        db.session.add(contact)
        db.session.commit()
        return contact

    def add_a_configuration(self):
        config_data = {
            "data": {
                "attributes": {
                    "label": "Test configuration",
                    "project_uri": "",
                    "project_name": "MOSES",
                    "status": "draft",
                    "start_date": "2021-10-22T09:31:00.000Z",
                    "end_date": "2021-10-31T09:32:00.000Z",
                    "hierarchy": [],
                },
                "type": "configuration",
            }
        }
        config = super().add_object(
            url=self.configurations_url,
            data_object=config_data,
            object_type=self.object_type,
        )
        config_id = config["data"]["id"]
        return config_id

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.configurations_url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
