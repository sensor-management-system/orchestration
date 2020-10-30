import unittest

from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.urls import base_url
from project.api.models.device import Device
from project.api.models.configuration import Configuration
from project.api.models.configuration_device import ConfigurationDevice
from project.api.models.configuration_platform import ConfigurationPlatform
from project.api.models.platform import Platform
from project.tests.read_from_json import extract_data_from_json_file


class TestConfigurationsService(BaseTestCase):
    """Tests for the Configurations Service."""
    configurations_url = base_url + '/configurations'
    platform_url = base_url + '/platforms'
    device_url = base_url + '/devices'
    object_type = 'configuration'
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = "/usr/src/app/project/tests/drafts/platforms_test_data.json"

    def test_get_configurations(self):
        """Ensure the GET /configurations route behaves correctly."""
        response = self.client.get(self.configurations_url)
        self.assertEqual(response.status_code, 200)

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
            platform=platform1, configuration=config1, offset_x=1.0,
            offset_y=1.0, offset_z=1.0
        )
        db.session.add(platform1_conf)

        platform2_conf = ConfigurationPlatform(
            platform=platform2,
            configuration=config1,
            parent_platform=platform1,
            offset_x=2.0, offset_y=2.0, offset_z=2.0
        )
        platform3_conf = ConfigurationPlatform(
            platform=platform3, configuration=config1, offset_x=13.5,
            offset_y=13.5, offset_z=13.5
        )

        db.session.add(platform2_conf)
        db.session.add(platform3_conf)

        device1_conf = ConfigurationDevice(
            device=device1, configuration=config1, parent_platform=platform2, offset_x=0.5,
            offset_y=0.5, offset_z=0.5
        )
        device2_conf = ConfigurationDevice(
            device=device2, configuration=config1, parent_platform=platform2, offset_x=0.6,
            offset_y=0.6, offset_z=0.6
        )
        device3_conf = ConfigurationDevice(
            device=device3, configuration=config1, parent_platform=platform2, offset_x=0.65,
            offset_y=0.65, offset_z=0.65
        )

        db.session.add(device1_conf)
        db.session.add(device2_conf)
        db.session.add(device3_conf)

        db.session.commit()

        c = db.session.query(Configuration).filter_by(label="Config1").first()

        self.assertEqual("static", c.location_type)

    def test_add_configuration(self):
        """Ensure POST a new configuration can be added to the database."""
        devices_json = extract_data_from_json_file(
            self.device_json_data_url,
            "devices")

        device_data = {
            "data": {
                "type": "device",
                "attributes": devices_json[0]}

        }
        super().add_object(
            url=self.device_url, data_object=device_data,
            object_type='device')

        platforms_json = extract_data_from_json_file(
            self.platform_json_data_url,
            "platforms")

        platform_data = {
            "data": {
                "type": "platform",
                "attributes": platforms_json[0]
            }
        }

        super().add_object(
            url=self.platform_url, data_object=platform_data,
            object_type='platform')

        config_json = extract_data_from_json_file(
            self.json_data_url,
            "configuration")

        device_data = {
            "data": {
                "type": "configuration",
                "attributes": config_json[0]}

        }
        super().add_object(
            url=self.configurations_url, data_object=device_data,
            object_type=self.object_type)


if __name__ == '__main__':
    unittest.main()
