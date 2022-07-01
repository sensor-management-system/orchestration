"""Tests for the mounting action timepoints controller for configuratins."""

import datetime

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    Platform,
    PlatformMountAction,
    User,
)
from project.api.models.base_model import db
from project.api.schemas.device_schema import DeviceSchema
from project.api.schemas.platform_schema import PlatformSchema
from project.tests.base import BaseTestCase


class TestControllerConfigurationMountingActionTimepoints(BaseTestCase):
    """Tests for the controller to get the timepoints for mounting actions."""

    def setUp(self):
        """Set up some example data that we will use in most of the tests."""
        super().setUp()
        contact = Contact(given_name="D", family_name="U", email="d.u@localhost")
        self.u = User(subject="du", contact=contact)

        self.configuration = Configuration(
            label="dummy configuration", is_internal=True
        )
        self.device1 = Device(
            short_name="Some device",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            device_type_name="Sensor",
        )
        self.platform1 = Platform(
            short_name="Some platform",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            platform_type_name="Sensor",
        )
        db.session.add_all(
            [contact, self.u, self.configuration, self.device1, self.platform1]
        )
        db.session.commit()
        self.url = (
            f"{base_url}/controller/configurations/"
            + f"{self.configuration.id}/mounting-action-timepoints"
        )

    def test_get_without_configuration_id(self):
        """Ensure that we get a 404 for a non existing configuration."""
        url = (
            f"{base_url}/controller/configurations/"
            + "999999/mounting-action-timepoints"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_interal_withoput_user(self):
        """Ensure anonymous can't access an internal configuration."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_empty(self):
        """Ensure we get an empty list if there is no mount."""
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_one_device_mount(self):
        """Ensure we get an entry for a device mount."""
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=self.device1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2022-05-18T12:00:00",
                "type": "device_mount",
                "attributes": DeviceSchema().dump(self.device1)["data"]["attributes"],
            }
        ]
        self.assertEqual(response.json, expected)

    def test_get_one_device_mount_with_unmount_date(self):
        """Ensure we get an entry for a device mount with unmount date."""
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=self.device1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
            end_date=datetime.datetime(2023, 5, 18, 12, 0, 0),
        )
        db.session.add(device_mount_action)
        db.session.commit()
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2022-05-18T12:00:00",
                "type": "device_mount",
                "attributes": DeviceSchema().dump(self.device1)["data"]["attributes"],
            },
            {
                "timepoint": "2023-05-18T12:00:00",
                "type": "device_unmount",
                "attributes": DeviceSchema().dump(self.device1)["data"]["attributes"],
            },
        ]
        self.assertEqual(response.json, expected)

    def test_get_one_platform_mount(self):
        """Ensure we get an entry for a platform mount."""
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=self.platform1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2021, 5, 10, 12, 13, 14),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2021-05-10T12:13:14",
                "type": "platform_mount",
                "attributes": PlatformSchema().dump(self.platform1)["data"][
                    "attributes"
                ],
            }
        ]
        self.assertEqual(response.json, expected)

    def test_get_one_platform_mount_with_unmount_date(self):
        """Ensure we get an entry for a platform mount with an unmount date."""
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=self.platform1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2021, 5, 10, 12, 13, 14),
            end_date=datetime.datetime(2021, 12, 10, 12, 13, 14),
        )
        db.session.add(platform_mount_action)
        db.session.commit()
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2021-05-10T12:13:14",
                "type": "platform_mount",
                "attributes": PlatformSchema().dump(self.platform1)["data"][
                    "attributes"
                ],
            },
            {
                "timepoint": "2021-12-10T12:13:14",
                "type": "platform_unmount",
                "attributes": PlatformSchema().dump(self.platform1)["data"][
                    "attributes"
                ],
            },
        ]
        self.assertEqual(response.json, expected)

    def test_get_multiple_mounts(self):
        """Ensure we get an entry for a platform mount with an unmount date."""
        platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration,
            platform=self.platform1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2020, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
        )
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration,
            device=self.device1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2021, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2023, 1, 1, 12, 0, 0),
        )
        device_mount_action2 = DeviceMountAction(
            configuration=self.configuration,
            device=self.device1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2024, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2025, 1, 1, 12, 0, 0),
        )
        db.session.add_all(
            [platform_mount_action1, device_mount_action1, device_mount_action2]
        )
        db.session.commit()
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "timepoint": "2020-01-01T12:00:00",
                "type": "platform_mount",
                "attributes": PlatformSchema().dump(self.platform1)["data"][
                    "attributes"
                ],
            },
            {
                "timepoint": "2021-01-01T12:00:00",
                "type": "device_mount",
                "attributes": DeviceSchema().dump(self.device1)["data"]["attributes"],
            },
            {
                "timepoint": "2022-01-01T12:00:00",
                "type": "platform_unmount",
                "attributes": PlatformSchema().dump(self.platform1)["data"][
                    "attributes"
                ],
            },
            {
                "timepoint": "2023-01-01T12:00:00",
                "type": "device_unmount",
                "attributes": DeviceSchema().dump(self.device1)["data"]["attributes"],
            },
            {
                "timepoint": "2024-01-01T12:00:00",
                "type": "device_mount",
                "attributes": DeviceSchema().dump(self.device1)["data"]["attributes"],
            },
            {
                "timepoint": "2025-01-01T12:00:00",
                "type": "device_unmount",
                "attributes": DeviceSchema().dump(self.device1)["data"]["attributes"],
            },
        ]
        self.assertEqual(response.json, expected)
