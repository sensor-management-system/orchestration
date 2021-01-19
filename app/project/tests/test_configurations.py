import datetime
import json
import unittest


from project import base_url
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.configuration_device import ConfigurationDevice
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.tests.base import BaseTestCase, create_token
from project.tests.read_from_json import extract_data_from_json_file


class TestConfigurationsService(BaseTestCase):
    """Tests for the Configurations Service."""

    configurations_url = base_url + "/configurations"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    object_type = "configuration"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_configurations(self):
        """Ensure the GET /configurations route behaves correctly."""
        response = self.client.get(self.configurations_url)
        self.assertEqual(response.status_code, 200)
        # There are no data sets inserted yet.
        self.assertEqual(response.json["data"], [])

    def test_add_configuration_model(self):
        """""Ensure Add Configuration model """

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

        c = db.session.query(Configuration).filter_by(label="Config1").first()
        self.assertEqual("static", c.location_type)

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


if __name__ == "__main__":
    unittest.main()
