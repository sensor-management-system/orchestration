import datetime
import os

from project import base_url
from project.api.models import Contact
from project.api.models import User
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.tests.base import BaseTestCase, test_file_path
from project.tests.base import create_token
from project.tests.base import fake, generate_userinfo_data
from project.tests.permissions import create_a_test_contact
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_generic_actions_models import generate_configuration_action_model
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

            config_data = {
                "data": {"type": "configuration", "attributes": config_json[0]}
            }
            _ = super().add_object(
                url=self.configurations_url,
                data_object=config_data,
                object_type=self.object_type,
            )

            # clean up after each run
            self.tearDown()

    def test_support_include_devices_and_platforms_on_rest_call(self):
        """
        Ensure that we can ask to include devices & platforms.

        When we ask for a configuration via the rest interface,
        we also want to query the devices & platforms together
        within this call.
        """
        # add a configuration, the same way as
        # in test_add_configuration_model
        platform1 = Platform(
            short_name="Platform 1",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        platform2 = Platform(
            short_name="Platform 2",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        platform3 = Platform(
            short_name="Platform 3",
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(platform1)
        db.session.add(platform2)
        db.session.add(platform3)

        device1 = Device(
            short_name="Device 1", is_public=False, is_private=False, is_internal=True,
        )
        device2 = Device(
            short_name="Device 2", is_public=False, is_private=False, is_internal=True,
        )
        device3 = Device(
            short_name="Device 3", is_public=False, is_private=False, is_internal=True,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.add(device3)

        config1 = Configuration(
            label="Config1", location_type="static", is_public=False, is_internal=True,
        )
        db.session.add(config1)
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
                        ["contacts", "src_longitude", "src_latitude", "src_elevation", ]
                    ),
                ]
            )
            access_headers = create_token()
            response = self.client.get(url, headers=access_headers)
            self.assertEqual(response.status_code, 200)
            data = response.json["data"]
            self.assertEqual(data["attributes"]["label"], config1.label)

    def test_delete_configuration_which_still_contains_actions(self):
        """
        Ensure that we can delete a configuration and it's
        included actions.

        """
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        device_parent_platform = Platform(
            short_name="device parent platform",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        platform = Platform(
            short_name=fake.linux_processor(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        parent_platform = Platform(
            short_name="platform parent-platform",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(subject="test_user@test.test", contact=contact)
        configuration = Configuration(
            label=fake.linux_processor(),
            is_public=False,
            is_internal=True,
            created_by=user,
        )
        db.session.add_all(
            [
                device,
                device_parent_platform,
                platform,
                parent_platform,
                contact,
                configuration,
                user,
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
        url = f"{self.configurations_url}/{configuration.id}"
        self.delete_as_owner(contact, user, url)

    def delete_as_owner(self, contact, user, url):
        token_data = {
            "sub": user.subject,
            "iss": "SMS unittest",
            "family_name": contact.family_name,
            "given_name": contact.given_name,
            "email": contact.email,
            "aud": "SMS",
        }
        access_headers = create_token(token_data)
        with self.client:
            response = self.client.delete(
                url, content_type="application/vnd.api+json", headers=access_headers
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_configuration_with_static_begin_location_action(self):
        """Ensure a configuration with a static_begin_location_action can be deleted"""
        configuration, contact, user = self.add_a_configuration_model()
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
                        "data": {"type": "configuration", "id": configuration.id}
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
        url_ = f"{self.configurations_url}/{configuration.id}"
        _ = self.delete_as_owner(contact, user, url_)

    def test_delete_configuration_with_static_end_location_action(self):
        """Ensure a configuration with a static_end_location_action can be deleted"""
        configuration, contact, user = self.add_a_configuration_model()

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
                        "data": {"type": "configuration", "id": configuration.id}
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
        url = f"{self.configurations_url}/{configuration.id}"
        _ = self.delete_as_owner(contact, user, url)

    def test_delete_configuration_with_dynamic_begin_location_action(self):
        """Ensure a configuration with a dynamic_begin_location_action can be deleted"""
        configuration, contact, user = self.add_a_configuration_model()

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
                        "data": {"type": "configuration", "id": configuration.id}
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
        url = f"{self.configurations_url}/{configuration.id}"
        _ = self.delete_as_owner(contact, user, url)

    def test_delete_configuration_with_dynamic_end_location_action(self):
        """Ensure a configuration with a dynamic_end_location_action can be deleted"""
        configuration, contact, user = self.add_a_configuration_model()

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
                        "data": {"type": "configuration", "id": configuration.id}
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
        url = f"{self.configurations_url}/{configuration.id}"
        _ = self.delete_as_owner(contact, user, url)


    def test_delete_configuration_with_generic_action(self):
        """Ensure a configuration with a generic action can be deleted"""

        configuration_action = generate_configuration_action_model()
        config_id = configuration_action.configuration_id
        _ = super().delete_object(url=f"{self.configurations_url}/{config_id}",)

    @staticmethod
    def add_a_contact():
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
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

    def add_a_configuration_model(self):
        contact = create_a_test_contact()

        user = User(subject=fake.email(), contact=contact)
        configuration = Configuration(
            label=fake.linux_processor(),
            is_public=False,
            is_internal=True,
            created_by=user,
        )
        db.session.add_all([contact, user, configuration])
        db.session.commit()
        return configuration, contact, user
